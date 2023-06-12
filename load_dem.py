"""
Load DEM Files for the map canvas extent from a static SRTM tile folder 
and create vrt mosaic if more than one tile was loaded.
"""

from qgis.core import *
from qgis.utils import iface
from qgis import processing
import os

# Path to SRTM
dem_folder  = '/media/riannek/Beryll/karten-data/SRTM/'

dem_grid = os.path.join(dem_folder, 'srtm_grid.gpkg')
dem_tiles = os.path.join(dem_folder, 'tiles')

# Style for DEM
dem_style = '/media/riannek/Beryll/karten-data/qgis-styles/Wanderkarte/dem-soft.qml'

def load_dem():
    # Open SRTM Grid
    print('Load SRTM Grid file')
    url = dem_grid
    url = url + '|layername=srtm_grid'
    layer = QgsVectorLayer(url, "SRTM Grid", "ogr")
    if not layer.isValid():
        iface.messageBar().pushWarning('DEM', 'Could not open SRTM Grid Geopackage')
        return None
    # Keep a reference of the layer style
    layerstyle = QgsMapLayerStyle()
    layerstyle.readFromLayer(layer)


    extent = iface.mapCanvas().extent()
    
    bbox = (str(extent.xMinimum()) + ',' +
        str(extent.xMaximum()) + ',' +
        str(extent.yMinimum()) + ',' +
        str(extent.yMaximum()) 
        + ' [' + QgsProject.instance().crs().authid() + ']'
        )
    print(bbox)

    # Get the polygons of the DEMs we need
    myresult = processing.run("native:extractbyextent", 
                                {'INPUT':layer,
                                'EXTENT':bbox,
                                'CLIP':False,
                                'OUTPUT':'TEMPORARY_OUTPUT'})
    layer = myresult['OUTPUT']

    for f in layer.getFeatures():
        print(f['id'])


    # Load the SRTM Tiles
    print('load SRTM tiles')
    demlayerlist = []

    for f in layer.getFeatures():
        filename = f['id'] + '.hgt'
        url = os.path.join(dem_tiles, filename)
        rlayer = QgsRasterLayer(url, f['id'])
        if not rlayer.isValid():
            print('Could not open DEM tile', f['id'])
        else:
            layer.dataProvider().deleteFeatures([f.id()])
            demlayerlist.append(rlayer)

    # Check result
    if layer.featureCount() > 0:
        print('Missing DEM tiles')
        iface.messageBar().pushWarning('DEM', 'There are' 
                + str(layer.featureCount()) + 'DEM tiles missing'  )
        layerstyle.writeToLayer(layer)
        QgsProject.instance().addMapLayer(layer)
        layer.setName('Missing DEM Tiles')
        for l in demlayerlist:
            QgsProject.instance().addMapLayer(l)
        return

    # Just in case:
    if len(demlayerlist) == 0:
        iface.messageBar().pushWarning('DEM', 'Something went wrong, failed to load DEM tiles.'  )
        return None

    # I want to add the DEM layer at the last position of TOC 
    root = QgsProject.instance().layerTreeRoot()
        
    if len(demlayerlist) == 1:
        rlayer = demlayerlist[0]
        QgsProject.instance().addMapLayer(rlayer, False) # False : Don't show layer yet
        root.addLayer(rlayer) # Append layer to layer tree
        rlayer.setName('DEM')
        
        if os.path.exists(dem_style ):
            rlayer.loadNamedStyle(dem_style)

        layertreelayer = root.findLayer(rlayer.id())
        layertreelayer.setExpanded(False)
        print('Successfully loaded 1 DEM tile')
    else:
        # Create virtual raster of DEM tiles
        print('Loaded', len(demlayerlist), 'DEM tiles')
        print('Create Virtual Raster and save it as DEM.vrt')
        url = os.path.splitext(QgsProject.instance().fileName())[0] + '_DEM.vrt'
        myresult = processing.runAndLoadResults("gdal:buildvirtualraster", 
                        {'INPUT':demlayerlist,
                        'RESOLUTION':0,'SEPARATE':False,
                        'PROJ_DIFFERENCE':False,
                        'ADD_ALPHA':False,
                        'ASSIGN_CRS':None,
                        'RESAMPLING':0,
                        'SRC_NODATA':'',
                        'EXTRA':'',
                        'OUTPUT':url})
        # Move to the bottom of the TOC
        currentlayername = os.path.splitext(os.path.basename(url))[0]
        rlayer = QgsProject.instance().mapLayersByName(currentlayername)[0]
        rlayer.setName('DEM')

        if os.path.exists(dem_style):
            rlayer.loadNamedStyle(dem_style)

        layertreelayer = root.findLayer(rlayer.id())
        layertreelayer.setExpanded(False)
        parent = layertreelayer.parent()
        myclone = layertreelayer.clone()
        root.addChildNode(myclone)
        parent.removeChildNode(layertreelayer)

load_dem()