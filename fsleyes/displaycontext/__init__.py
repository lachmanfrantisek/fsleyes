#!/usr/bin/env python
#
# __init__.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""The ``displaycontext`` package contains classes which define the display
options for pretty much everything in *FSLeyes*.  


.. note:: Before perusing this package, you should read the high level
          overview in the :mod:`~fsl.fsleyes` package documentation. Go on -
          it won't take you too long.


--------
Overview
--------


The most important classes defined in this package are:

  - the :class:`.DisplayContext` class, which defines how all of the
    overlays in an :class:`.OverlayList` should be displayed.

  - the :class:`.Display` class, which defines how a single overlay should be
    displayed.

  - the :class:`.DisplayOpts` base class, and its sub-classes, which define
    overlay type specific options.


A :class:`.DisplayContext` instance encapsulates an :class:`.OverlayList`, and
defines how the overlays in the list should be displayed.  Each
:class:`.ViewPanel` displayed in *FSLeyes* (e.g. the :class:`.OrthoPanel`) has
its own ``DisplayContext`` instance; a ``ViewPanel`` uses its
``DisplayContext`` instance to configure general display properties, and also
to access the :class:`.Display` properties for individual overlays.


All of the classes mentioned on ths page are defined in sub-modules, but are
imported into, and are thus available from, the ``displaycontext`` package
namespace. For example::

    import fsleyes.displaycontext as fsldc

    # The VolumeOpts class is defined in the
    # fsleyes.displaycontext.volumeopts
    # module, but is available in the 
    # fsleyes.displaycontext namespace.
    volopts = fsldc.VolumeOpts(overlay, display, overlayList, displayCtx)


-----------------------
Overlay display options
-----------------------


The :class:`.Display` class, and the :class:`.DisplayOpts` sub-classes define
how to display a single overlay. Options common to all overlays
(e.g. :attr:`.Display.brightness`, :attr:`.Display.alpha`) are defined in the
``Display`` class, whereas options which are specific to a particular overlay
type (e.g. :attr:`.VolumeOpts.cmap`, :attr:`.LineVectorOpts.lineWidth`) are
defined in the corresponding :class:`.DisplayOpts` sub-class.


The ``Display`` instance for a particular overlay owns and manages a single
``DisplayOpts`` instance - whenever the overlay display type is changed, the
``Display`` instance deletes the old ``DisplayOpts`` instance, and creates a
new one accordingly.  The following ``DisplayOpts`` sub-classes exist:

.. autosummary::
   :nosignatures:

   ~fsleyes.displaycontext.volumeopts.NiftiOpts
   ~fsleyes.displaycontext.volumeopts.VolumeOpts
   ~fsleyes.displaycontext.maskopts.MaskOpts
   ~fsleyes.displaycontext.vectoropts.VectorOpts
   ~fsleyes.displaycontext.vectoropts.RGBVectorOpts
   ~fsleyes.displaycontext.vectoropts.LineVectorOpts
   ~fsleyes.displaycontext.modelopts.ModelOpts
   ~fsleyes.displaycontext.labelopts.LabelOpts
   ~fsleyes.displaycontext.tensoropts.TensorOpts
   ~fsleyes.displaycontext.shopts.SHOpts


--------------
Overlay groups
--------------


.. note:: Support for overlay groups is quite basic at this point in time. See
          the :class:`.OverlayListPanel` for details.

The :mod:`~.displaycontext.group` module provides the functionality to
link the display properties of one or more overlays. One or more
:class:`.OverlayGroup` instances may be added to the
:attr:`.DisplayContext.overlayGroups` list.


-------------
Scene options
-------------


Independent of the ``DisplayContext``, ``Display`` and ``DisplayOpts``
classes, the ``displaycontext`` package is also home to a few classes which
define *scene* options:


.. autosummary::
   :nosignatures:

   ~fsleyes.displaycontext.canvasopts.SliceCanvasOpts
   ~fsleyes.displaycontext.canvasopts.LightBoxCanvasOpts
   ~fsleyes.displaycontext.sceneopts.SceneOpts
   ~fsleyes.displaycontext.orthoopts.OrthoOpts
   ~fsleyes.displaycontext.lightboxopts.LightBoxOpts


.. note:: Aside from an increase in code modularity and cleanliness, another
          reason that all of these scene display settings are separated from
          the things that use them is so they can be imported, queried, and
          set without having to import the modules that use them.

          For example, the :mod:`.fsleyes_parseargs` module needs to be able
          to access all of the display settings in order to print out the
          corresponding help documentation. This process would take much
          longer if ``fsleyes_parseargs`` had to import, e.g.
          :class:`.OrthoPanel`, which would result in importing both :mod:`wx`
          and :mod:`.OpenGL`.

          Keeping these display settings separate allows us to avoid these
          time-consuming imports in situations where they are not needed.
"""


import itertools          as it
import fsl.utils.typedict as td
import fsl.data.constants as constants

from .               import display
from .displaycontext import DisplayContext
from .display        import Display
from .group          import OverlayGroup
from .sceneopts      import SceneOpts
from .orthoopts      import OrthoOpts
from .lightboxopts   import LightBoxOpts
from .volumeopts     import NiftiOpts
from .volumeopts     import VolumeOpts
from .maskopts       import MaskOpts
from .vectoropts     import VectorOpts
from .vectoropts     import RGBVectorOpts
from .vectoropts     import LineVectorOpts
from .modelopts      import ModelOpts
from .labelopts      import LabelOpts
from .tensoropts     import TensorOpts
from .shopts         import SHOpts

from .displaycontext import InvalidOverlayError


OVERLAY_TYPES = td.TypeDict({

    'Image'        : ['volume',     'mask',  'rgbvector',
                      'linevector', 'label', 'sh', 'tensor'],
    'Model'        : ['model'],
    'DTIFitTensor' : ['tensor', 'rgbvector', 'linevector'],
})
"""This dictionary provides a mapping between all overlay classes,
and the possible values that the :attr:`Display.overlayType` property
may take for each of them. 

For each overlay class, the first entry in the corresponding overlay type
list is used as the default overlay type.
"""


ALL_OVERLAY_TYPES = list(set(it.chain(*OVERLAY_TYPES.values())))
"""This attribute contains a list of all possible overlay types - see the
:attr:`.Display.overlayType` property and tge :data:`.display.OVERLAY_TYPES`
dictionary for more details.
"""


DISPLAY_OPTS_MAP = {
    'volume'     : VolumeOpts,
    'rgbvector'  : RGBVectorOpts,
    'linevector' : LineVectorOpts,
    'mask'       : MaskOpts,
    'model'      : ModelOpts,
    'label'      : LabelOpts,
    'tensor'     : TensorOpts,
    'sh'         : SHOpts,
}
"""This dictionary provides a mapping between each overlay type, and
the :class:`DisplayOpts` subclass which contains overlay type-specific
display options.
"""


def getOverlayTypes(overlay):
    """Returns a list of possible overlay types for the given overlay.
    This is a wrapper around the :attr:`OVERLAY_TYPES` dictionary, which
    might adjust the returned list based on properties of the overlay.
    """

    import fsl.data.image as fslimage
    from . import            shopts
    
    possibleTypes = list(OVERLAY_TYPES[overlay])

    if not isinstance(overlay, fslimage.Image):
        return possibleTypes

    shape = overlay.shape

    # Could this image be a vector image?
    couldBeVector = len(shape) == 4 and shape[-1] == 3

    # Or could it be a SH or tensor image?
    couldBeTensor = len(shape) == 4 and shape[-1] == 6 
    couldBeSH     = len(shape) == 4 and shape[-1] in shopts.SH_COEFFICIENT_TYPE

    # Special cases:
    #
    # If the overlay looks like a vector image,
    # and its nifti intent code is set as such,
    # make rgbvector the default overlay type
    if couldBeVector:
        if overlay.intent == constants.NIFTI_INTENT_RGB_VECTOR:
            possibleTypes.remove(   'rgbvector')
            possibleTypes.remove(   'linevector')
            possibleTypes.insert(0, 'linevector')
            possibleTypes.insert(0, 'rgbvector')
        
    # Otherwise, remove the vector options
    else:
        
        try:               possibleTypes.remove('rgbvector')
        except ValueError: pass

        try:               possibleTypes.remove('linevector')
        except ValueError: pass

    if not couldBeSH:
        try:               possibleTypes.remove('sh')
        except ValueError: pass

    if not couldBeTensor:
        try:               possibleTypes.remove('tensor')
        except ValueError: pass 

    return possibleTypes
