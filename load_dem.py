"""
Load DEM Files for the map canvas extent from a static SRTM tile folder 
and create vrt mosaic if more than one tile was loaded. Don't forget to 
set the dem_folder variable below before using the script.
"""

from qgis.core import *
from qgis.utils import iface
from qgis import processing
import os

# Set the path to SRTM here:
dem_folder  = '/media/riannek/Beryll/karten-data/SRTM/tiles'


# Get the path to the SRTM grid geopackage. 
try:
    # Does not work in the python console
    script_path = os.path.dirname(__file__)
except NameError:
    # This code only works in the QGIS python console
    # if running the script from the tab editor.
    from console.console import _console
    script_path = os.path.dirname(_console.console.tabEditorWidget.currentWidget().path)



dem_grid = os.path.join(script_path, 'srtm_grid.gpkg')
    
print(dem_grid) 



def load_dem():
    # Open SRTM Grid
    print('Load SRTM Grid file')
    url = dem_grid + '|layername=srtm_grid'
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
        url = os.path.join(dem_folder, filename)
        rlayer = QgsRasterLayer(url, f['id'])
        if not rlayer.isValid():
            print('Could not open DEM tile', f['id'])
        else:
            layer.dataProvider().deleteFeatures([f.id()])
            demlayerlist.append(rlayer)

    # Check result
    if layer.featureCount() > 0:
        print('Missing DEM tiles')
        iface.messageBar().pushWarning('DEM', 'There are ' 
                + str(layer.featureCount()) + ' DEM tiles missing'  )
        layerstyle.writeToLayer(layer)
        QgsProject.instance().addMapLayer(layer)
        layer.setName('Missing DEM Tiles')
        for l in demlayerlist:
            QgsProject.instance().addMapLayer(l)
        return

    # Just in case:
    if len(demlayerlist) == 0:
        iface.messageBar().pushWarning('DEM', 'Something went wrong, failed to load DEM tiles. Check the folder name in the script.'  )
        return None

    # I want to add the DEM layer at the last position of TOC 
    root = QgsProject.instance().layerTreeRoot()
        
    if len(demlayerlist) == 1:
        rlayer = demlayerlist[0]
        QgsProject.instance().addMapLayer(rlayer, False) # False : Don't show layer yet
        root.addLayer(rlayer) # Append layer to layer tree
        rlayer.setName('DEM')
        layertreelayer = root.findLayer(rlayer.id())
        layertreelayer.setExpanded(False)
        print('Successfully loaded 1 DEM tile')
    else:
        # Create virtual raster of DEM tiles
        print('Loaded', len(demlayerlist), 'DEM tiles')
        print('Create Virtual Raster and save it as DEM.vrt')
        # Get the folder of the project
        url = os.path.splitext(QgsProject.instance().fileName())[0]
        if url == '':
            iface.messageBar().pushWarning('DEM', 'You did not save the project, creating DRM.vrt in the current working directory ' + os.getcwd())
            url = 'DEM.vrt'
        else:
            url = url + '_DEM.vrt'
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

        layertreelayer = root.findLayer(rlayer.id())
        layertreelayer.setExpanded(False)
        parent = layertreelayer.parent()
        myclone = layertreelayer.clone()
        root.addChildNode(myclone)
        parent.removeChildNode(layertreelayer)



# Load DEM
load_dem()