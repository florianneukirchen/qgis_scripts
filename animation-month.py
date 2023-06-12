"""
Set time range of layers to a month taken from the layer name.

Use copy_paste_this_ramp(layers) to copy ramp from active layer.

"""

re_pattern = r'(\d*).tif$'

# Use one of the layer selections: 
# layers = iface.layerTreeView().selectedLayers() # Selected layers
layers = iface.mapCanvas().layers() # Checked layers
#layers = QgsProject.instance().mapLayers().values() # All Layers

c_ramp_name = 'RdYlGn'
c_ramp_invert = True

dummy_year = 2020


def time_range(month):
    start = QDateTime(QDate(dummy_year, month, 1), QTime(0, 0, 0))
    if month < 12:
        end = QDateTime(QDate(dummy_year, month + 1, 1), QTime(0, 0, 0))
    else:
        end = QDateTime(QDate(dummy_year + 1, 1, 1), QTime(0, 0, 0))
    return QgsDateTimeRange(start, end)
    
def nr_from_layername(layer):
    return int(re.search(re_pattern, layer.name()).group(1))
    
def set_timerange(layers):
    print('set time range')
    for layer in layers:
        prop = layer.temporalProperties()
        month = nr_from_layername(layer)
        print(month)
        range = time_range(month)
        prop.setIsActive(True)
        prop.setMode(prop.ModeFixedTemporalRange)
        prop.setFixedTemporalRange(range)

       

def get_min_max(layers):
    print('get min max')
    minvalues = []
    maxvalues = []
    for layer in layers:
        provider = layer.dataProvider()
        extent = layer.extent()
        band = 1 # Assume single band for now
        stats = provider.bandStatistics(band, QgsRasterBandStats.All, extent, 0)
        minvalues.append(stats.minimumValue)
        maxvalues.append(stats.maximumValue)
        
    return min(minvalues), max(maxvalues)
    
    
def set_pseudocolorrenderer(layers, minv, maxv):
    print('set pseudocolor')
    band = 1
    c_ramp = QgsStyle.defaultStyle().colorRamp(c_ramp_name).clone()
    if c_ramp_invert:
        c_ramp.invert()

    for layer in layers:
        print(layer.name())
        func = QgsColorRampShader()
        func.setSourceColorRamp(c_ramp.clone())

        shader = QgsRasterShader()
        shader.setRasterShaderFunction(func)

        renderer = QgsSingleBandPseudoColorRenderer(
            layer.dataProvider(),
            band,
            shader
        )
        
        renderer.setClassificationMax(maxv)
        renderer.setClassificationMin(minv)
        
        func.classifyColorRamp()

        layer.setRenderer(renderer)

        layer.triggerRepaint()
        iface.layerTreeView().refreshLayerSymbology(layer.id())


def copy_paste_this_ramp(layers):
    a_layer = iface.activeLayer()
    ramp = a_layer.renderer().shader().rasterShaderFunction().sourceColorRamp()
    
    for layer in layers:
        if layer.id() != a_layer.id():
            renderer = layer.renderer()
            shader = renderer.shader()
            func = shader.rasterShaderFunction()
            func.setSourceColorRamp(ramp.clone())
            func.classifyColorRamp()
            shader.setRasterShaderFunction(func)
            layer.triggerRepaint()
            iface.layerTreeView().refreshLayerSymbology(layer.id())
            

            

minv, maxv = get_min_max(layers)
set_pseudocolorrenderer(layers, minv, maxv)

set_timerange(layers)


print('Done')