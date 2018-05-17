#!/usr/bin/env python
#
# notebook.py - The NotebookAction class.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module provides the :class:`NotebookAction` class, an action which
starts an IPython kernel and a Jupyter notebook server, allowing the user
to interact with FSLeyes via a jupyter notebook.
"""


import               os
import os.path    as op
import subprocess as sp
import               time
import               atexit
import               shutil
import               logging
import               tempfile
import               warnings
import               threading
import               webbrowser

import               wx
import jinja2     as j2

import fsleyes_widgets.utils.progress as progress
import fsleyes_widgets.utils.status   as status
import fsl.utils.settings             as settings
import fsl.utils.idle                 as idle

import                                   fsleyes
import fsleyes.strings                as strings
from . import                            base
from . import                            runscript

try:
    import                            zmq

    import zmq.eventloop.zmqstream as zmqstream
    import tornado.ioloop          as ioloop

    import ipykernel.ipkernel      as ipkernel
    import ipykernel.zmqshell      as zmqshell
    import ipykernel.heartbeat     as heartbeat

    import IPython.core.magic      as magic

    import jupyter_client          as jc
    import jupyter_client.session  as jcsession

    ENABLED = True

except ImportError:
    ENABLED = False


log = logging.getLogger(__name__)


# Debug during development
log.setLevel(logging.DEBUG)


logging.getLogger('jupyter_client').setLevel(logging.DEBUG)
# logging.getLogger('ipykernel')     .setLevel(logging.DEBUG)
logging.getLogger('notebook')      .setLevel(logging.DEBUG)


class NotebookAction(base.Action):
    """The ``NotebookAction`` is an :class:`.Action` which (if necessary)
    starts an embedded IPython kernel and a jupyter notebook server, and
    opens the server home page in a web browser allowing the user to interact
    with FSLeyes via notebooks.
    """


    def __init__(self, overlayList, displayCtx, frame):
        """Create a ``NotebookAction``.

        :arg overlayList: The :class:`.OverlayList`.
        :arg displayCtx:  The master :class:`.DisplayContext`.
        :arg frame:       The :class:`.FSLeyesFrame`.
        """
        base.Action.__init__(self, self.__openNotebooks)

        # permanently disable if any
        # dependencies are not present
        self.enabled        = ENABLED
        self.__overlayList  = overlayList
        self.__displayCtx   = displayCtx
        self.__frame        = frame
        self.__kernel       = None
        self.__server       = None


    def __openNotebooks(self):
        """Called when this ``NotebookAction`` is invoked. Starts the
        server and kernel if necessary, then opens a new notebook in a
        web browser.
        """

        # have the kernel or server threads crashed?
        if self.__kernel is not None and not self.__kernel.is_alive():
            self.__kernel = None
        if self.__server is not None and not self.__server.is_alive():
            self.__server = None

        # show a progress dialog if we need
        # to initialise the kernel or server
        if self.__kernel is None or self.__server is None:
            progdlg = progress.Bounce()
        else:
            progdlg = None

        try:
            # start the kernel/server, and show
            # an error if something goes wrong
            errt = strings.titles[  self, 'init.error']
            errm = strings.messages[self, 'init.error']
            with status.reportIfError(errt, errm):
                if self.__kernel is None:
                    self.__kernel = self.__startKernel(progdlg)
                if self.__server is None:
                    self.__server = self.__startServer(progdlg)

        finally:
            if progdlg is not None:
                progdlg.Destroy()
                progdlg = None

        # if all is well, open the
        # notebook server homepage
        webbrowser.open('http://localhost:{}'.format(self.__server.port))


    def __bounce(self, secs, progdlg):
        """Used by :meth:`__startKernel` and :meth:`__startServer`. Blocks for
        from ipykernel.kernelapp import IPKernelApp``secs``, bouncing
        the :class:`.Progress` dialog ten times per second, and yielding to
        the ``wx`` main loop.
        """
        for i in range(int(secs * 10)):
            progdlg.DoBounce()
            wx.Yield()
            time.sleep(0.1)


    def __startKernel(self, progdlg):
        """Attempts to create and start a :class:`BackgroundIPythonKernel`.

        :returns: the kernel if it was started.

        :raises: A :exc:`RuntimeError` if the kernel did not start.
        """
        progdlg.UpdateMessage(strings.messages[self, 'init.kernel'])
        kernel = BackgroundIPythonKernel(
            self.__frame,
            self.__overlayList,
            self.__displayCtx)
        kernel.start()
        self.__bounce(1, progdlg)

        if not kernel.is_alive():
            raise RuntimeError('Could not start IPython kernel: '
                               '{}'.format(kernel.error))

        return kernel


    def __startServer(self, progdlg):
        """Attempts to create and start a :class:`NotebookServer`.

        :returns: the server if it was started.

        :raises: A :exc:`RuntimeError` if the serer did not start.
        """

        progdlg.UpdateMessage(strings.messages[self, 'init.server'])
        server = NotebookServer(self.__kernel.connfile,
                                self.__overlayList,
                                self.__displayCtx,
                                self.__frame)
        server.start()
        self.__bounce(1.5, progdlg)

        if not server.is_alive():
            raise RuntimeError('Could not start notebook server: '
                               '{}'.format(server.stderr))

        return server


class BackgroundIPythonKernel(threading.Thread):
    """The BackgroundIPythonKernel creates an IPython jupyter kernel and makes
    it accessible over tcp (on the local machine only). The ``zmq`` event loop
    is run on a separate thread, but the kernel handles events on the main
    thread, via :func:`.idle.idle`.


    The Jupyter/IPython documentation is quite fragmented at this point in
    time; `this github issue <https://github.com/ipython/ipython/issues/8097>`_
    was useful in figuring out the implementation details.
    """


    def __init__(self, overlayList, displayCtx, frame):
        """Set up the kernel and ``zmq`` ports. A jupyter connection file
        containing the information needed to connect to the kernel is saved
        to a temporary file - its path is accessed as an attribute
        called :meth:`connfile`.

        :arg overlayList: The :class:`.OverlayList`.
        :arg displayCtx:  The master :class:`.DisplayContext`.
        :arg frame:       The :class:`.FSLeyesFrame`.
        """

        threading.Thread.__init__(self)

        self.daemon        = True
        ip                 = '127.0.0.1'
        transport          = 'tcp'
        addr               = '{}://{}'.format(transport, ip)
        self.__connfile    = None
        self.__ioloop      = None
        self.__kernel      = None
        self.__error       = None
        self.__frame       = frame
        self.__overlayList = frame
        self.__displayCtx  = frame

        env = runscript.fsleyesScriptEnvironment(
            frame,
            overlayList,
            displayCtx)[1]

        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=DeprecationWarning)

            self.__heartbeat = heartbeat.Heartbeat(
                zmq.Context(), (transport, ip, 0))
            self.__heartbeat.start()

            # Use an empty key to disable message signing
            session = jcsession.Session(key=b'')
            context = zmq.Context.instance()

            # create sockets for kernel communication
            shellsock   = context.socket(zmq.ROUTER)
            iopubsock   = context.socket(zmq.PUB)
            controlsock = context.socket(zmq.ROUTER)

            shellport   = shellsock  .bind_to_random_port(addr)
            iopubport   = iopubsock  .bind_to_random_port(addr)
            controlport = controlsock.bind_to_random_port(addr)
            hbport      = self.__heartbeat.port

            shellstrm   = zmqstream.ZMQStream(shellsock)
            controlstrm = zmqstream.ZMQStream(controlsock)

            # Create the kernel
            self.__kernel = ipkernel.IPythonKernel.instance(
                shell_class=FSLeyesIPythonShell,
                session=session,
                shell_streams=[shellstrm, controlstrm],
                iopub_socket=iopubsock,
                user_ns=env,
                log=logging.getLogger('ipykernel.kernelbase'))

        # write connection file to a temp dir
        hd, fname = tempfile.mkstemp(
            prefix='fsleyes-kernel-{}.json'.format(os.getpid()),
            suffix='.json')
        os.close(hd)

        self.__connfile = fname

        log.debug('IPython kernel connection file: %s', fname)

        jc.write_connection_file(
            fname,
            shell_port=shellport,
            iopub_port=iopubport,
            control_port=controlport,
            hb_port=hbport,
            ip=ip)

        atexit.register(os.remove, self.__connfile)


    @magic.line_magic
    def fsleyes_init(self):
        """
        """
        pass


    @property
    def kernel(self):
        """The ``IPythonKernel`` object. """
        return self.__kernel


    @property
    def connfile(self):
        """The jupyter connection file containing information to connect
        to the IPython kernel.
        """
        return self.__connfile


    @property
    def error(self):
        """If an error occurs on the background thread causing it to crash,
        a reference to the ``Exception`` is stored here.
        """
        return self.__error


    def __kernelDispatch(self):
        """Event loop used for the IPython kernel. Submits the kernel function
        to the :func:`.idle.idle` loop, and schedules another call to this
        method on the ``zmq`` event loop.

        This means that, while the ``zmq`` loop runs in its own thread, the
        IPython kernel is executed on the main thread.
        """

        idle.idle(self.__kernel.do_one_iteration)
        self.__ioloop.call_later(self.__kernel._poll_interval,
                                 self.__kernelDispatch)


    def run(self):
        """Start the IPython kernel and Run the ``zmq`` event loop. """

        try:
            self.__ioloop = ioloop.IOLoop()
            self.__ioloop.make_current()
            self.__kernel.start()
            self.__ioloop.call_later(self.__kernel._poll_interval,
                                     self.__kernelDispatch)
            self.__ioloop.start()

        except Exception as e:
            self.__error = e
            raise


class FSLeyesIPythonShell(zmqshell.ZMQInteractiveShell):
    """Custom IPython shell class used by FSLeyes. """

    def enable_gui(self, gui):
        """Overrides  ``ipykernel.zmqshell.ZMQInteractiveShell.enable_gui``.

        The default implementation will attempt to change the IPython GUI
        integration event loop, which will conflict with our own event loop
        in the :class:`BackgroundIPythonKernel`. So this implementation
        does nothing.
        """
        pass


class NotebookServer(threading.Thread):
    """Thread which starts a jupyter notebook server, and waits until
    it dies or is killed.

    The server is configured such that all notebooks will connect to
    the same kernel, specified by the ``kernelFile`` parameter to
    :meth:`__init__`.
    """


    def __init__(self, kernelFile, overlayList, displayCtx, frame):
        """Create a ``NotebookServer`` thread.

        :arg kernelFile:  JSON connection file of the jupyter kernel
                          to which all notebooks should connect.
        :arg overlayList: The :class:`.OverlayList`.
        :arg displayCtx:  The master :class:`.DisplayContext`.
        :arg frame:       The :class:`.FSLeyesFrame`.
        """

        threading.Thread.__init__(self)
        self.daemon        = True
        self.__kernelFile  = kernelFile
        self.__overlayList = overlayList
        self.__displayCtx  = displayCtx
        self.__frame       = frame
        self.__stdout      = None
        self.__stderr      = None
        self.__port        = settings.read('fsleyes.notebook.port', 8888)


    @property
    def port(self):
        """Returns the TCP port that the notebook server is listening on. """
        return self.__port


    @property
    def stdout(self):
        """After the server has died, returns its standard output. While the
        server is still running, returns ``None``.
        """
        return self.__stdout


    @property
    def stderr(self):
        """After the server has died, returns its standard error. While the
        server is still running, returns ``None``.
        """
        return self.__stderr


    def run(self):
        """Sets up a server configuration file, and then calls
        ``jupyer-notebook`` via ``subprocess.Popen``. Waits until
        the notebook process dies.
        """

        # copy our custom jupyter config template
        # directory to a temporary location that
        # will be deleted on exit.
        cfgdir = op.join(tempfile.mkdtemp(prefix='fsleyes-jupyter'), 'config')

        cfgdir = '/Users/paulmc/Projects/fsleyes/config-{}'.format(os.getpid())

        shutil.copytree(op.join(fsleyes.assetDir, 'assets', 'jupyter'), cfgdir)

        self.__initConfigDir(cfgdir)

        # Set up the environment in which the
        # server will run - make sure FSLeyes
        # is on the PYTHONPATH, and
        # JUPYTER_CONFIG_DIR is set, so our
        # custom bits and pieces will be found.
        env        = dict(os.environ)
        pythonpath = os.pathsep.join((cfgdir, env['PYTHONPATH']))

        env['JUPYTER_CONFIG_DIR'] = cfgdir
        env['PYTHONPATH']         = pythonpath

        # command to start the notebook
        # server in a sub-process
        self.__nbproc = sp.Popen(['jupyter-notebook'],
                                 # stdout=sp.PIPE,
                                 # stderr=sp.PIPE,
                                 cwd=cfgdir,
                                 env=env)

        def killServer():
            # We need two CTRL+Cs to kill
            # the notebook server
            self.__nbproc.terminate()
            self.__nbproc.terminate()
            # shutil.rmtree(op.abspath(op.join(cfgdir, '..')))

        # kill the server when we get killed
        atexit.register(killServer)

        # wait forever
        o, e          = self.__nbproc.communicate()
        self.__stdout = o.decode()
        self.__stderr = e.decode()



    def __initConfigDir(self, cfgdir):
        """
        """

        # Environment for generating a jupyter
        # notebook server configuration file
        cfgenv = {
            'fsleyes_nbserver_port'       : self.__port,
            'fsleyes_nbserver_dir'        : op.expanduser('~'),
            'fsleyes_nbserver_static_dir' : cfgdir,
            'fsleyes_nbextension_dir'     : op.join(cfgdir, 'nbextensions'),
            'fsleyes_kernel_connfile'     : self.__kernelFile,
        }

        # Environment for generating the
        # notebook template extension
        extenv = {
            'fsleyes_md_intro'  : '# FSLeyes notebook',
            'fsleyes_code_init' : 'print(\'hi!\')',
        }

        cfgfile = op.join(cfgdir, 'jupyter_notebook_config.py')
        extfile = op.join(cfgdir, 'nbextensions', 'notebook_template.js')

        files = [cfgfile, extfile]
        envs  = [cfgenv,  extenv]

        for fn, e in zip(files, envs):
            with open(fn, 'rt') as f: template = j2.Template(f.read())
            with open(fn, 'wt') as f: f.write(template.render(**e))
