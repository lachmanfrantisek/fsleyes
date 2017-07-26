#!/usr/bin/env python
#
# overlaydisplaypanel.py - The OverlayDisplayPanel.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>

"""This module provides the :class:`OverlayDisplayPanel` class, a *FSLeyes
control* panel which allows the user to change overlay display settings.
"""


import logging
import functools
import collections

import fsleyes_props                  as props

import fsleyes.strings                as strings
import fsleyes.tooltips               as fsltooltips
import fsleyes.panel                  as fslpanel

from . import overlaydisplaywidgets   as odwidgets


log = logging.getLogger(__name__)


class OverlayDisplayPanel(fslpanel.FSLeyesSettingsPanel):
    """The ``OverlayDisplayPanel`` is a :Class:`.FSLeyesPanel` which allows
    the user to change the display settings of the currently selected
    overlay (which is defined by the :attr:`.DisplayContext.selectedOverlay`
    property). The display settings for an overlay are contained in the
    :class:`.Display` and :class:`.DisplayOpts` instances associated with
    that overlay. An ``OverlayDisplayPanel`` looks something like the
    following:

    .. image:: images/overlaydisplaypanel.png
       :scale: 50%
       :align: center

    An ``OverlayDisplayPanel`` uses a :class:`.WidgetList` to organise the
    settings into two main sections:

      - Settings which are common across all overlays - these are defined
        in the :class:`.Display` class.

      - Settings which are specific to the current
        :attr:`.Display.overlayType` - these are defined in the
        :class:`.DisplayOpts` sub-classes.


    The settings that are displayed on an ``OverlayDisplayPanel`` are
    defined in the :attr:`_DISPLAY_PROPS` and :attr:`_DISPLAY_WIDGETS`
    dictionaries.
    """


    def __init__(self, parent, overlayList, displayCtx, frame):
        """Create an ``OverlayDisplayPanel``.

        :arg parent:      The :mod:`wx` parent object.
        :arg overlayList: The :class:`.OverlayList` instance.
        :arg displayCtx:  The :class:`.DisplayContext` instance.
        :arg frame:       The :class:`.FSLeyesFrame` instance.
        """

        fslpanel.FSLeyesSettingsPanel.__init__(self,
                                               parent,
                                               overlayList,
                                               displayCtx,
                                               frame,
                                               kbFocus=True)

        displayCtx .addListener('selectedOverlay',
                                 self._name,
                                 self.__selectedOverlayChanged)
        overlayList.addListener('overlays',
                                 self._name,
                                 self.__selectedOverlayChanged)

        self.__viewPanel      = parent
        self.__widgets        = None
        self.__currentOverlay = None

        self.__selectedOverlayChanged()


    def destroy(self):
        """Must be called when this ``OverlayDisplayPanel`` is no longer
        needed. Removes property listeners, and calls the
        :meth:`.FSLeyesPanel.destroy` method.
        """

        self._displayCtx .removeListener('selectedOverlay', self._name)
        self._overlayList.removeListener('overlays',        self._name)

        if self.__currentOverlay is not None and \
           self.__currentOverlay in self._overlayList:

            display = self._displayCtx.getDisplay(self.__currentOverlay)

            display.removeListener('overlayType', self._name)

        self.__viewPanel      = None
        self.__widgets        = None
        self.__currentOverlay = None

        fslpanel.FSLeyesPanel.destroy(self)


    def __selectedOverlayChanged(self, *a):
        """Called when the :class:`.OverlayList` or
        :attr:`.DisplayContext.selectedOverlay` changes. Refreshes this
        ``OverlayDisplayPanel`` so that the display settings for the newly
        selected overlay are shown.
        """
        from fsleyes.views.scene3dpanel import Scene3DPanel

        vp          = self.__viewPanel
        overlay     = self._displayCtx.getSelectedOverlay()
        lastOverlay = self.__currentOverlay
        widgetList  = self.getWidgetList()

        if overlay is None:
            self.__currentOverlay = None
            self.__widgets        = None
            widgetList.Clear()
            self.Layout()
            return

        if overlay is lastOverlay:
            return

        self.__currentOverlay = overlay
        self.__widgets        = collections.OrderedDict()

        display = self._displayCtx.getDisplay(overlay)
        opts    = display.getDisplayOpts()

        if isinstance(vp, Scene3DPanel):
            groups  = ['display', 'opts', '3d']
            targets = [ display,   opts,   opts]
            labels  = [strings.labels[self, display],
                       strings.labels[self, opts],
                       strings.labels[self, '3d']]

        else:
            groups  = ['display', 'opts']
            targets = [ display,   opts]
            labels  = [strings.labels[self, display],
                       strings.labels[self, opts]]

        keepExpanded = {g : True for g in groups}

        if lastOverlay is not None and \
           lastOverlay in self._overlayList:

            lastDisplay = self._displayCtx.getDisplay(lastOverlay)
            lastDisplay.removeListener('overlayType', self._name)

        if lastOverlay is not None:
            for g in groups:
                keepExpanded[g] = widgetList.IsExpanded(g)

        display.addListener('overlayType', self._name, self.__ovlTypeChanged)

        widgetList.Clear()

        for g, l, t in zip(groups, labels, targets):

            widgetList.AddGroup(g, l)
            self.__widgets[g] = self.updateWidgets(t, g)
            widgetList.Expand(g, keepExpanded[g])

        self.setNavOrder()
        self.Layout()


    def setNavOrder(self):

        allWidgets = self.__widgets.items()
        allWidgets = functools.reduce(lambda a, b: a + b, allWidgets)

        fslpanel.FSLeyesSettingsPanel.setNavOrder(self, allWidgets)


    def __ovlTypeChanged(self, *a):
        """Called when the :attr:`.Display.overlayType` of the current overlay
        changes. Refreshes the :class:`.DisplayOpts` settings which are shown,
        as a new :class:`.DisplayOpts` instance will have been created for the
        overlay.
        """

        opts       = self._displayCtx.getOpts(self.__currentOverlay)
        widgetList = self.getWidgetList()

        self.__widgets[opts] = self.updateWidgets(opts, 'opts')

        widgetList.RenameGroup('opts', strings.labels[self, opts])

        if '3d' in self.__widgets:
            self.__widgets['3d'] = self.updateWidgets(opts, '3d')

        self.setNavOrder()
        self.Layout()


    def updateWidgets(self, target, groupName):
        """Called by the :meth:`__selectedOverlayChanged` and
        :meth:`__ovlTypeChanged` methods. Re-creates the controls on this
        ``OverlayDisplayPanel`` for the specified group.

        :arg target:    A :class:`.Display` or :class:`.DisplayOpts` instance,
                        which contains the properties that controls are to be
                        created for.

        :arg groupName: Either ``'display'`` or ``'opts'``/``'3d'``,
                        corresponding to :class:`.Display` or
                        :class:`.DisplayOpts` properties.

        :returns:       A list containing all of the new widgets that
                        were created.
        """

        widgetList = self.getWidgetList()

        widgetList.ClearGroup(groupName)

        if groupName == '3d':
            dispProps = odwidgets.get3DPropertyList(target)
            dispSpecs = odwidgets.get3DWidgetSpecs( target)
        else:
            dispProps = odwidgets.getPropertyList(target)
            dispSpecs = odwidgets.getWidgetSpecs( target)

        allLabels     = []
        allTooltips   = []
        allWidgets    = []
        allContainers = []

        for p in dispProps:

            spec  = dispSpecs[p]

            specs    = [spec]
            labels   = [strings    .properties.get((target, p), None)]
            tooltips = [fsltooltips.properties.get((target, p), None)]

            if callable(spec):

                # Will either return a contsiner
                # widget/sizer and a list of widgets
                # for setting the navigation order,
                # or will return a list of specs
                # (with an irrelevant second parameter)
                container, widgets = spec(
                    target,
                    widgetList,
                    self,
                    self.getOverlayList(),
                    self.getDisplayContext())

                if isinstance(container, collections.Sequence):
                    specs    = container
                    keys     = [s.key for s in specs]
                    labels   = [strings.properties.get((target, k), None)
                                for k in keys]
                    tooltips = [fsltooltips.properties.get((target, k), None)
                                for k in keys]

                else:
                    allContainers.append(container)
                    allWidgets   .extend(widgets)
                    specs = []

            for s in specs:
                widget = props.buildGUI(widgetList, target, s)

                allWidgets   .append(widget)
                allContainers.append(widget)

            allLabels  .extend(labels)
            allTooltips.extend(tooltips)

        for widget, label, tooltip in zip(allContainers,
                                          allLabels,
                                          allTooltips):
            if label is None:
                label = ''
            widgetList.AddWidget(
                widget,
                label,
                tooltip=tooltip,
                groupName=groupName)

        self.Layout()

        return allWidgets
