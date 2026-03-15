from qgis.core import (
    QgsVectorFileWriter,
    QgsCoordinateTransformContext,
    QgsMapLayer
)
import os

# Edit file path here 
gpkg_path = r"C:/temp/weitere.gpkg"
 
selected_layers = iface.layerTreeView().selectedLayers()
 
if not selected_layers:
    raise Exception("No layer selected!")
 
first_layer = True
 
for layer in selected_layers:
 
    if layer.type() != QgsMapLayer.VectorLayer:
        print(f"Skipped (no vector layer): {layer.name()}")
        continue
 
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GPKG"
    options.layerName = layer.name()
 
    if first_layer:
        # Create GPKG
        options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile
        first_layer = False
    else:
        # Add more layers
        options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
 
    result = QgsVectorFileWriter.writeAsVectorFormatV3(
        layer,
        gpkg_path,
        QgsCoordinateTransformContext(),
        options
    )
 
    error = result[0] if isinstance(result, tuple) else result
 
    if error == QgsVectorFileWriter.NoError:
        print(f"Saved: {layer.name()}")
    else:
        print(f"Error with {layer.name()} (Code: {error})")
 
print("Finished.")