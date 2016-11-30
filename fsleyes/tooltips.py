#!/usr/bin/env python
#
# tooltips.py - Tooltips for FSLeyes.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains tooltips used throughout *FSLeyes*.

Tooltips are stored in :class:`.TypeDict` dictionariesa, broadly organised
into the following categories:

 ================== ================================================
 :data:`properties` Tooltips for ``props.HasProperties`` properties.
 :data:`actions`    Tooltips for :class:`.ActionProvider` actions.
 :data:`misc`       Tooltips for everything else.
 ================== ================================================

The :func:`initTooltips` function initialises some parameters controlling
tooltip display. It is called by the :class:`.FSLeyesFrame` upon creation.
"""


from fsl.utils.typedict import TypeDict


def initTooltips():
    """Sets some parameters controlling tooltip display. """
    import wx
    wx.ToolTip.Enable(     True)
    wx.ToolTip.SetDelay(   1500)
    wx.ToolTip.SetMaxWidth(300)
    wx.ToolTip.SetReshow(  3000)
    wx.ToolTip.SetAutoPop( 5000)


properties = TypeDict({

    # DisplayContext

    'DisplayContext.displaySpace'     : 'The space in which overlays are '
                                        'displayed.',
    'DisplayContext.radioOrientation' : 'If checked, images oriented to the '
                                        'MNI152 standard will be displayed in '
                                        'radiological orientation (i.e. with '
                                        'subject left to the right of the '
                                        'display, and subject right to the '
                                        'left). Otherwise they will be '
                                        'displayed in neurological '
                                        'orientation (i.e. with subject left '
                                        'to the left of the display).', 

    # Overlay Display
    
    'Display.name'        : 'The name of this overlay.',
    'Display.overlayType' : 'The overlay type - how this overlay should be '
                            'displayed.',
    'Display.enabled'     : 'Show/hide this overlay.',
    'Display.alpha'       : 'The opacity of this overlay.',
    'Display.brightness'  : 'The brightness of this overlay. For volume '
                            'overlays, brightness is applied as a linear '
                            'offset to the display range.',
    'Display.contrast'    : 'The contrast of this overlay. For volume '
                            'overlay, contrast is applied as a linear '
                            'scaling factor to the display range.',

    # Overlay DisplayOpts

    'NiftiOpts.volume'     : 'The volume number (for 4D images).',
    'NiftiOpts.resolution' : 'Spatial display resolution, in mm.',
    'NiftiOpts.transform'  : 'The affine transformation matrix to apply '
                             'to this image. You can choose to display '
                             'the image without any transformation (as if '
                             'the image voxels are 1mm isotropic); or you '
                             'can choose to scale the voxels by the pixdim '
                             'values in the NIFTI header; or you can choose '
                             'to apply the affine transformation as defined '
                             'in the NIFTI header.',

    'VolumeOpts.displayRange'    : 'Data display range - the low value '
                                   'corresponds to the low colour, and the '
                                   'high value to the high colour, in the '
                                   'selected colour map.',
     
    'VolumeOpts.clippingRange'   : 'Data clipping range - voxels with values '
                                   'outside of this range will not be '
                                   'displayed.',
    'VolumeOpts.invertClipping'  : 'Invert the clipping range, so that voxels '
                                   'inside the range are not displayed, and '
                                   'voxels outside of the range are '
                                   'displayed. ' 
                                   'This option is useful for displaying '
                                   'statistic images.',
    'VolumeOpts.cmap'            : 'The colour map to use.',
    'VolumeOpts.negativeCmap'    : 'The colour map to use for negative '
                                   'values.',
    'VolumeOpts.useNegativeCmap' : 'Enable the negative colour map - '
                                   'this allows positive and negative '
                                   'values to be coloured independently.',
    'VolumeOpts.cmapResolution'  : 'Colour map resolution - the number of '
                                   'colours to use in the colour maps.', 
 
    'VolumeOpts.interpolation'   : 'Interpolate the image data for display '
                                   'purposes. You can choose no  '
                                   'interpolation (equivalent to nearest '
                                   'neighbour interpolation), linear '
                                   'interpolation, or third-order spline '
                                   '(cubic) interpolation.',
    'VolumeOpts.invert'          : 'Invert the display range, so that the low '
                                   'value corresponds to the high colour, and '
                                   'vice versa.',
    'VolumeOpts.enableOverrideDataRange' : 'Override the actual data range of '
                                           'an image with a user-specified '
                                           'one. This is useful for images '
                                           'which have a very large data '
                                           'range that is driven by outliers.',
    'VolumeOpts.overrideDataRange'       : 'Override the actual data range of '
                                           'an image with a user-specified '
                                           'one. This is useful for images '
                                           'which have a very large data '
                                           'range that is driven by outliers.',

    'MaskOpts.colour'    : 'The colour of this mask image.',
    'MaskOpts.invert'    : 'Invert the mask threshold range, so that values '
                           'outside of the range are shown, and values '
                           'within the range are hidden.',
    'MaskOpts.threshold' : 'The mask threshold range - values outside of '
                           'this range will not be displayed.',

    'LabelOpts.lut'          : 'The lookup table to use for this label image.',
    'LabelOpts.outline'      : 'Show the outline of each labelled region '
                               'only. If unchecked, labelled regions are '
                               'filled.',
    'LabelOpts.outlineWidth' : 'If showing label outlines, this setting '
                               'controls the outline width (as a proportion '
                               'of the image voxel size). If showing filled '
                               'regions, this setting controls the size of a '
                               'transparent border around each region. In '
                               'this situation, setting the width to 0 will '
                               'prevent the border from being shown.',
    'LabelOpts.showNames'    : 'Annotate the image display with the names of '
                               'each labelled region.',

    'VectorOpts.xColour'          : 'The colour corresponding to the X '
                                    'component of the vector - the brightness '
                                    'of the colour corresponds to the '
                                    'magnitude of the X component. This '
                                    'option has no effect if a colour image '
                                    'is selected.', 
    'VectorOpts.yColour'          : 'The colour corresponding to the Y '
                                    'component of the vector - the brightness '
                                    'of the colour corresponds to the '
                                    'magnitude of the Y component. This '
                                    'option has no effect if a colour image '
                                    'is selected.', 
    'VectorOpts.zColour'          : 'The colour corresponding to the Z '
                                    'component of the vector - the brightness '
                                    'of the colour corresponds to the '
                                    'magnitude of the Z component. This '
                                    'option has no effect if a colour image '
                                    'is selected.',
    'VectorOpts.suppressX'        : 'Ignore the X vector component when '
                                    'colouring voxels. This option has no '
                                    'effect if a colour image is selected.', 
    'VectorOpts.suppressY'        : 'Ignore the Y vector component when '
                                    'colouring voxels. This option has no '
                                    'effect if a colour image is selected.', 
    'VectorOpts.suppressZ'        : 'Ignore the Z vector component when '
                                    'colouring voxels. This option has no '
                                    'effect if a colour image is selected.',
    'VectorOpts.suppressMode'     : 'When a vector direction is suppressed,'
                                    'it\'s contribution to the resulting '
                                    'will be replaced according to this '
                                    'setting.', 
    'VectorOpts.modulateImage'    : 'Modulate the vector colour brightness by '
                                    'another image. The image selected here '
                                    'is normalised to lie in the range (0, '
                                    '1), and the brightness of each vector '
                                    'colour is scaled by the corresponding '
                                    'modulation value before it is coloured. '
                                    'The modulation image must have the same '
                                    'voxel dimensions as the vector image.',
    'VectorOpts.clipImage'        : 'Clip vector voxels according to the '
                                    'values in another image. Vector voxels '
                                    'which correspond to values in the '
                                    'clipping image that have a value less '
                                    'than the current clipping threshold are '
                                    'not shown. The clipping image must have '
                                    'the same voxel dimensions as the vector '
                                    'image. ',
    'VectorOpts.colourImage'      : 'Colour the vectors according to the '
                                    'values in another image, and by the '
                                    'selected colour map. The colour image '
                                    'must have the same voxel dimensions as '
                                    'the vector image. ',
    'VectorOpts.clippingRange'    : 'Vector values which have a corresponding '
                                    'clipping image value that is outside of '
                                    'this range are not displayed. ',
    'VectorOpts.modulateRange'    : 'The data range that is used when '
                                    'modulating vector brightness by a '
                                    'modulation image.', 
    'VectorOpts.cmap'             : 'Colour map to use for colouring vector '
                                    'voxels, if a colour image is selected.',
    'VectorOpts.orientFlip'       : 'If checked, direction orientations '
                                    'within each voxel are flipped about '
                                    'the x axis.', 
    'LineVectorOpts.lineWidth'    : 'The width of each vector line, in '
                                    'display pixels.',
    'LineVectorOpts.directed'     : 'If unchecked, the vector data is assumed '
                                    'to be undirected - the vector line at '
                                    'each voxel is scaled to have a length of '
                                    '1mm, and is centered within the voxel so '
                                    'that it passes through the voxel centre.'
                                    'If this option is checked, the vector '
                                    'data is assumed to be directed - each '
                                    'vector line begins at the voxel centre, '
                                    'and is scaled to have length 0.5mm.',
    'LineVectorOpts.unitLength'   : 'If checked, the vector lines are scaled '
                                    'so that they have a length of 1mm (times'
                                    'the length scaling factor). '
                                    'Otherwise the vector lengths are '
                                    'unmodified.',
    'LineVectorOpts.lengthScale'  : 'Scale the vector line length by this '
                                    'scaling factor (expressed as a '
                                    'percentage).', 
    'RGBVectorOpts.interpolation' : 'Interpolate the vector data for display '
                                    'purposes. You can choose none '
                                    '(equivalent to nearest-neighbour), '
                                    'linear, or spline interpolation.',

    'ModelOpts.colour'       : 'The colour of the model.',
    'ModelOpts.outline'      : 'If checked, only the outline of the model is '
                               'displayed. Otherwise the model is filled. ',
    'ModelOpts.outlineWidth' : 'If the model outline is being displayed, this '
                               'setting controls the outline width.',
    'ModelOpts.showName'     : 'Annotate the display wiuh the model name.',
    'ModelOpts.refImage'     : 'If this model was derived from a volumetric '
                               'image, you can choose that image as a '
                               'reference. The displayed model will then be '
                               'transformed according to the '
                               'transformation/orientation settings of the '
                               'reference.',
    'ModelOpts.coordSpace'   : 'If a reference image is selected, this '
                               'setting defines the space, relative to the '
                               'reference image, in which the model '
                               'coordinates are defined.',

    'TensorOpts.lighting'         : 'If enabled, a simple lighting model is '
                                    'used to highlight the tensor '
                                    'orientations.', 
    'TensorOpts.tensorResolution' : 'This setting controls the number of '
                                    'vertices used to render each tensor. '
                                    'A higher value will result in better '
                                    'looking tensors, but may reduce ' 
                                    'performance.' ,
    'TensorOpts.tensorScale'      : 'By default, the tensor radii are scaled '
                                    'the largest eigenvalue of the tensor '
                                    'matrix, so that the largest tensor is '
                                    'drawn to fit within a voxel. This '
                                    'setting allows the tensor scale to be '
                                    'adjusted.',

    'SHOpts.lighting'         : 'If enabled, a simple lighting model is used '
                                'to highlight the FODs',
    'SHOpts.size'             : 'This setting allows the FOD size to be '
                                'scaled up or down',
    'SHOpts.radiusThreshold'  : 'This setting allows FODs with small radius '
                                'to be hidden.',
    'SHOpts.shResolution'     : 'This setting controls the display resolution '
                                '(number of vertices) used to draw each FOD.',
    'SHOpts.shOrder'          : 'This setting controls the maximum spherical '
                                'harmonic function order with which to '
                                'display FODs.',
    'SHOpts.colourMode'       : 'FODs can be coloured according to their '
                                'radius/size, or according to their '
                                'orientation/direction. This setting is '
                                'disabled when you choose to colour the FODs '
                                'by another image (e.g. a FA map).',
    
    # SceneOpts

    'SceneOpts.showCursor'         : 'Show/hide the cursor which highlights '
                                     'the current location.',
    'SceneOpts.cursorGap'          : 'Show a gap at the cursor centre.',
    'SceneOpts.cursorColour'       : 'Colour of the location cursor.',
    'SceneOpts.bgColour'           : 'Canvas background colour.',
    'SceneOpts.showColourBar'      : 'If the currently selected overlay is a '
                                     'volumetric image, show a colour bar '
                                     'depicting the colour/data display '
                                     'range.',
    'SceneOpts.colourBarLocation'  : 'Where to display the colour bar.',
    'SceneOpts.colourBarLabelSide' : 'What side of the colour bar to draw the '
                                     'colour bar labels.',
    'SceneOpts.performance'        : 'Rendering performance - 1 gives the '
                                     'fastest, but at the cost of lower '
                                     'display quality, and some display '
                                     'limitations. 5 gives the best '
                                     'display quality, but may be too slow on '
                                     'some older systems.',

    'OrthoOpts.showXCanvas' : 'Show / hide the X canvas '
                              '(sagittal in MNI space).',
    'OrthoOpts.showYCanvas' : 'Show / hide the Y canvas '
                              '(coronal in MNI space).',
    'OrthoOpts.showZCanvas' : 'Show / hide the Z canvas '
                              '(axial in MNI space).',
    'OrthoOpts.showCursor'  : 'Show/hide the location cross-hairs.',
    'OrthoOpts.showLabels'  : 'If the currently selected overlay is a NIFTI '
                              'image, show / hide anatomical orientation '
                              'labels.',
    'OrthoOpts.labelSize'   : 'Scale the label font size.',
    'OrthoOpts.layout'      : 'How to lay out each of the three canvases.',
    'OrthoOpts.zoom'        : 'Zoom level for all three canvases.',

    'LightBoxOpts.zoom'           : 'Zoom level - this controls how many '
                                    'slices to display.',
    'LightBoxOpts.sliceSpacing'   : 'The spacing between adjacent slices. '
                                    'The units and range of this setting '
                                    'depend upon the currently selected '
                                    'overlay.',
    'LightBoxOpts.zrange'         : 'The start/end points of the displayed '
                                    'range of slices. The units and range '
                                    'of this setting depend upon the '
                                    'currently selected overlay.',
    'LightBoxOpts.zax'            : 'Slices along this axis will be '
                                    'displayed.',
    'LightBoxOpts.showGridLines'  : 'If checked, lines will be shown between '
                                    'each slice.',
    'LightBoxOpts.highlightSlice' : 'If checked, a box will be drawn around '
                                    'the currently selected slice.',

    # ViewPanels

    'CanvasPanel.syncLocation'       : 'If checked, the location shown on '
                                       'this panel will be linked to the '
                                       'location shown on other panels (as '
                                       'long as they also have this setting '
                                       'enabled).',
    'CanvasPanel.syncOverlayOrder'   : 'If checked, the order in which '
                                       'overlays are displayed on this '
                                       'panel will be linked to order shown '
                                       'on other panels (as long as they '
                                       'also have this setting enabled). ',
    'CanvasPanel.syncOverlayDisplay' : 'If checked, the display properties '
                                       'of all overlays shown in this panel '
                                       'linked to the display properties '
                                       'on other panels (as long as they '
                                       'also have this setting enabled). ',
    'CanvasPanel.movieMode'          : 'If checked, the volume of '
                                       'the currently selected overlay '
                                       'will automatically change at a rate '
                                       'determined by the movie rate. If you '
                                       'want several overlays to be animated, '
                                       'group them using the overlay list.',
    'CanvasPanel.movieRate'          : 'The rate at which volumes are changed '
                                       'when movie mode is enabled. Low = '
                                       'fast, and high = slow.', 

    'PlotPanel.legend'     : 'Show / hide a legend for series which have '
                             'been added to the plot.',
    'PlotPanel.xAutoScale' : 'If checked, the plot X axis limits are '
                             'automatically adjusted whenever the plot '
                             'contents change.',
    'PlotPanel.yAutoScale' : 'If checked, the plot Y axis limits are '
                             'automatically adjusted whenever the plot '
                             'contents change.', 
    'PlotPanel.xLogScale'  : 'If checked, a log (base 10) scale is used for '
                             'the x axis.',
    'PlotPanel.yLogScale'  : 'If checked, a log (base 10) scale is used for '
                             'the y axis.',
    'PlotPanel.ticks'      : 'Show / hide axis ticks and tick labels.',
    'PlotPanel.grid'       : 'Show hide plot grid.' ,
    'PlotPanel.gridColour' : 'Set the plot grid colour.' ,
    'PlotPanel.bgColour'   : 'Set the plot background colour.' ,
    'PlotPanel.smooth'     : 'Smooth displayed data series (with cubic spline '
                             'interpolation).',
    'PlotPanel.xlabel'     : 'Set the x axis label.',
    'PlotPanel.ylabel'     : 'Set the y axis label.',
    'PlotPanel.limits'     : 'Manually set the x/y axis limits.',

    'TimeSeriesPanel.usePixdim'        : 'If checked, the x axis data is '
                                         'scaled by the time dimension pixdim '
                                         'value specified in the NIFTI '
                                         'header.',
    'TimeSeriesPanel.plotMelodicICs'   : 'If checked, the component time '
                                         'courses are plotted for Melodic '
                                         'images. If not checked, Melodic '
                                         'images are treated as regular 4D '
                                         'images.',
    'TimeSeriesPanel.plotMode'         : 'Plotting mode. You can choose to: '
                                         '\n  - Display the data as-is.'
                                         '\n  - Remove the temporal mean from '
                                         'the data before plotting.'
                                         '\n  - Scale the data to the range '
                                         '[-1, 1].'
                                         '\n  - Scale the data to percent '
                                         'signal-changed, relative to the '
                                         'temporal mean.',
    'TimeSeriesPanel.currentColour'    : 'Colour of the current time series.',
    'TimeSeriesPanel.currentAlpha'     : 'Opacity of the current time series.',
    'TimeSeriesPanel.currentLineWidth' : 'Line width of the current time '
                                         'series.',
    'TimeSeriesPanel.currentLineStyle' : 'Line style of the current time '
                                         'series.', 

    'HistogramPanel.histType'    : 'Show histogram data as raw counts, or '
                                   'as probabilities.',

    'PowerSpectrumPanel.plotFrequencies'  : 'If checked, the x values '
                                            'are transformed into frequency '
                                            'values.',
    'PowerSpectrumPanel.plotMelodicICs'   : 'If checked, the component power '
                                            'spectra are plotted for Melodic '
                                            'images. If not checked, Melodic '
                                            'images are treated as regular 4D '
                                            'images.',

    # DataSeries

    'DataSeries.enabled'   : 'Show/hide the line.',
    'DataSeries.colour'    : 'Line colour.',
    'DataSeries.alpha'     : 'Line opacity.',
    'DataSeries.label'     : 'Line label (shown in the legend).',
    'DataSeries.lineWidth' : 'Line width.',
    'DataSeries.lineStyle' : 'Line style.',

    'FEATTimeSeries.plotData'         : 'Plot the input data.',
    'FEATTimeSeries.plotFullModelFit' : 'Plot the full model fit.',
    'FEATTimeSeries.plotResiduals'    : 'Plot the residuals of the full '
                                        'model fit.', 
    'FEATTimeSeries.plotEVs'          : 'Plot the EV (explanatory variable) '
                                        'time courses.',
    'FEATTimeSeries.plotPEFits'       : 'Plot the model fit to each PE '
                                        '(parameter estimate).',
    'FEATTimeSeries.plotCOPEFits'     : 'Plot the model fit to each COPE '
                                        '(Contrast of Parameter Estimates).',
    'FEATTimeSeries.plotPartial'      : 'Plot the raw data, after regression '
                                        'against the selected PE/COPE.',

    'HistogramSeries.autoBin'         : 'If checked, automatically calculate '
                                        'the number of bins to use in the '
                                        'histogram calculation.', 
    'HistogramSeries.nbins'           : 'Number of bins to use in the '
                                        'histogram calculation (not '
                                        'applicable  if auto-binning is '
                                        'enabled).',
    'HistogramSeries.ignoreZeros'     : 'Ignore zeros in the histogram '
                                        'calculation.', 
    'HistogramSeries.showOverlay'     : 'Show a 3D mask overlay highlighting '
                                        'voxels which have been included in '
                                        'the histogram.',
    'HistogramSeries.includeOutliers' : 'Include values which are outside of '
                                        'the data range - they are added to '
                                        'the first and last bins.',
    'HistogramSeries.volume'          : 'Current volume to calculate the '
                                        'histogram for (4D images only).',
    'HistogramSeries.dataRange'       : 'Data range to include in the '
                                        'histogram.',


    'PowerSpectrumSeries.varNorm'     : 'If checked, the data is demeaned and '
                                        'normalised by its standard deviation '
                                        'before its power spectrum is '
                                        'calculated via a fourier transform.', 

    # Profiles

    'OrthoPanel.profile'                      : 'Switch between view mode '
                                                'and edit mode',

    'OrthoEditProfile.selectionCursorColour'  :
    'Colour to use for the selection cursor.',
    
    'OrthoEditProfile.selectionOverlayColour' :
    'Colour to use to highlight selected regions.',

    'OrthoEditProfile.drawMode' : 
    'Toggle between "draw" mode and "select" mode. In draw mode, you can '
    'simply \'draw\' on an image - when you release the mouse, the voxel '
    'values are replaced with the current fill value (or erased). Select '
    'mode is more powerful, but requires two steps to edit an image - '
    'you must first select some voxels, and then fill/erase them.',
    
    'OrthoEditProfile.mode' :
    'Switch between editing tools. The "Navigate" tool simply allows you to '
    'view the image and change the display location. The "Pencil" tool allows '
    'you to fill voxel values (in draw mode), or to manually select voxels '
    '(in select mode). The "Erase" tool allows you to erase voxel values (in '
    'draw mode), or to deselect voxels (in select mode). When select mode is '
    'enabled, the "select by intensity" tool allows you to select voxels '
    'based on their intensity. Click on a "seed" voxel, and all voxels with '
    'a similar intenstiy to that seed voxel will be selected.',
    
    'OrthoEditProfile.selectionSize' :
    'Size (in voxels) of the selection region when using the pencil or '
    'eraser tools.',
    
    'OrthoEditProfile.selectionIs3D' :
    'When using the pencil or eraser tools, choose between a 2D square '
    'selection in the plane of the active canvas, or a 3D cuboid. With '
    'the select by intensity tool, you can limit the selection search to '
    'the current 2D slice, or extend the search to the full 3D image.',

    'OrthoEditProfile.fillValue' :
    'Value to replace voxels with when drawing/filling.',

    'OrthoEditProfile.eraseValue' :
    'Value to replace voxels with when erasing.' , 
    
    'OrthoEditProfile.intensityThres' :
    'When using the select by intensity tool, this is the threshold used to '
    'determine whether or not a voxel should be selected. If the difference '
    'in intensity between the seed voxel and another voxel in the search '
    'space is less than or equal to this threshold, the voxel will be '
    'selected.',

    'OrthoEditProfile.intensityThresLimit' :
    'Upper limit for the intensity threshold. By default the upper intensity '
    'threshold limit is calculated from he image data range, but you can '
    'manually adjust it through this setting.',
    
    'OrthoEditProfile.localFill' :
    'When using the select by intensity tool, this setting will cause the '
    'search space to be limited to voxels which have a similar intensity '
    'to the seed voxel, and which are adjacent to another selected voxel.',
    
    'OrthoEditProfile.limitToRadius' :
    'When using the select by intensity tool, this setting will cause the '
    'search limited to a circle or sphere of the specified radius.',
    
    'OrthoEditProfile.searchRadius' :
    'When using the select by intensity tool, if the search is being limited '
    'to a radius, this setting allows you to specify the radius of the search '
    'circle/sphere.',

    'OrthoEditProfile.targetImage' : \
    'Choose the target image for edit operations. By default, when you '
    'fill/erase voxels, the currently selected image is modified. However, '
    'you can select a different image (of the same dimensions and resolution '
    'as the currently selected image) as the target for edit operations. This '
    'is most useful when selecting voxels by intensity - you can select voxels'
    'based on the values in the currently selected image, but then fill/erase '
    'that selection in another image.', 
})


actions = TypeDict({
    'CanvasPanel.screenshot'        : 'Take a screenshot of the current scene',
    'CanvasPanel.toggleDisplayPanel' : 'Show more overlay display settings',
    'CanvasPanel.toggleCanvasSettingsPanel' : 'Show more view '
                                              'control settings',
    'CanvasPanel.toggleOverlayInfo' : 'Show/hide the overlay '
                                      'information panel.',

    'OrthoPanel.toggleEditPanel' : 'Show/hide the edit settings panel',

    'PlotPanel.screenshot'       : 'Take a screenshot of the current plot.',
    'PlotPanel.importDataSeries' : 'Import data series from a text file.',
    'PlotPanel.exportDataSeries' : 'Export data series to a text file.',
    'PlotPanel.addDataSeries'    : 'Add (hold) data series '
                                   'from the current overlay.',
    'PlotPanel.removeDataSeries' : 'Remove the most recently '
                                   'added data series.',

    'TimeSeriesPanel.toggleTimeSeriesControl' : 'Show/hide the time '
                                                'series control panel.',
    'TimeSeriesPanel.togglePlotList'          : 'Show/hide the time '
                                                'series list panel.',
    'HistogramPanel.toggleHistogramControl'   : 'Show/hide the histogram '
                                                'control panel.',
    'HistogramPanel.togglePlotList'           : 'Show/hide the histogram '
                                                'list panel.',
    
    'PowerSpectrumPanel.togglePowerSpectrumControl' : 'Show/hide the power '
                                                      'spectrum control '
                                                      'panel.',
    'PowerSpectrumPanel.togglePlotList'             : 'Show/hide the power '
                                                      'spectrum list '
                                                      'panel.', 
 

    'OrthoViewProfile.resetDisplay' : 'Reset the display on all canvases.',
    'OrthoViewProfile.centreCursor' : 'Reset location to centre of scene',

    'OrthoEditProfile.undo' : 
    'Undo the most recent action. A history of changes to the selection, '
    'and to image data, are maintained. separate undo/redo histories are '
    'maintained for each image.',
    
    'OrthoEditProfile.redo' :
    'Redo the most recent undone action.',
    
    'OrthoEditProfile.createMask' :
    'Create an empty 3D mask image which has the same dimensions as the '
    'currently selected image.',

    'OrthoEditProfile.clearSelection' :
    'Clear the current selection - no voxels are selected.',
    
    'OrthoEditProfile.fillSelection' :
    'Fill selected voxels in the currently selected '
    'image with the current fill value. ',
    
    'OrthoEditProfile.eraseSelection' :
    'Set the value at all selected voxels in the currently selected '
    'image to zero.',

    'OrthoEditProfile.copySelection' :
    'Copy the values of all selected voxels in the currently selected image '
    'and store them in an internal clipboard. The voxel values can then be '
    'pasted into another image (which has the same dimensions/resolution as '
    'the source image).',

    'OrthoEditProfile.pasteSelection' :
    'Paste the contents of the clipboard into the currently selected image.',

    'VolumeOpts.resetDisplayRange' :
    'Reset the display range to the data range.',

    # Items in the OverlayListPanel
    'ListItemWidget.save'  : 'Save this overlay to a file',
    'ListItemWidget.group' : 'Link some properties of this overlay '
                             'with other linked overlays (e.g. '
                             'volume)',
})



misc = TypeDict({
    'PlotControlPanel.labels' : 'X/Y axis labels.',
    'PlotControlPanel.xlim'   : 'X axis data limits.',
    'PlotControlPanel.ylim'   : 'Y axis data limits.'
})
