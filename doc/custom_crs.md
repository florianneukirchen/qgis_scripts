Module custom_crs
=================
The script defines functions that can be used in the QGIS python console to speed up the generation of custom projections 
for the region of interest, including:
- Orthographic projection (i.e. view from space) 
- Satellite view (a.k.a. tilted perspective projection or general perspective)
- Lambert azimuthal equal-area projection (LAEA)
- Lambert conformal conic (LCC)
- Albers equal-area conic projection
- Robinson / Miller / Mollweide / Winkel Tripel or other projections centered on the Pacific or any custom longitude

For example, the following line creates a custom CRS (and an autogenerated description of the CRS) that mimics the view of Peru 
from a satellite in a height of 5500 km above 25°S, 70°W, looking towards -20° from north direction with a tilt of 30° away from nadir
(nice for small insets showing the area of interest): 

crs, desc = crs_sat(-25, -70, h=5500000, azi=-20, tilt=30, setproject=True) 

With setproject=True, the CRS of the project is set accordingly. This makes it very easy to adjust the values and to find 
the best angles. To save the CRS, pass the option savecrs=True while creating the custom crs or call the function save_crs(crs, desc) with an existing one.

The class AreaOfInterest() provides an alternative approach. To define your area 
of interest, either choose a layer comprising only your area (the layer extend 
will be used) or select some features of a vector layer (the bounding box of 
selected features will be used). Now initiate an instance of the class:

aoi = AreaOfInterest()

And create a Lambert azimuthal equal-area projection centered of the center of 
the area of interest with:

crs = aoi.laea()

It is possible to override certain attributes and to round the values. For an 
Albers projection with standard parallels rounded to 2 digits and longitude 
centered on 0°:

aoi.albers(lon_0=0, round_digits=2)

The default is to set the project CRS to any newly created CRS. To change this 
behavior, set 

aoi.setproject = False 

You can save the CRS that was created last as user CRS to be used in other projects:

aoi.save_crs()

Functions
---------

    
`crs_albers(lat_1, lat_2, lon_0=0, setproject=False, savecrs=False)`
:   Create a custom Albers equal-area conic projection with standard parallels lat_1 and lat_2. 
    
    Note: The greatest accuracy is obtained if the selected standard parallels enclose two-thirds the height of the map.
    Parameters:
        lat_1 (float): First standard parallel (degrees)
        lat_2 (float): Second standard parallel (degrees)
        lon_0=0 (float): Longitude of map center (degrees)
        setproject=False: Use the CRS to set the project CRS
        savecrs=False: Save the custom CRS in the database 
    Returns:
        crs (QgsCoordinateReferenceSystem)
        description (str)

    
`crs_laea(lat, lon, setproject=False, savecrs=False)`
:   Create a custom Lambert azimuthal equal-area projection centered on lat, lon. 
    
    Parameters:
        lat (float): Latitude (degrees)
        lon (float): Longitude (degrees)
        setproject=False: Use the CRS to set the project CRS
        savecrs=False: Save the custom CRS in the database 
    Returns:
        crs (QgsCoordinateReferenceSystem)
        description (str)

    
`crs_lcc(lat_1=33, lat_2=45, lon_0=0, setproject=False, savecrs=False)`
:   Create a custom Lambert conformal conic (LCC)  projection with standard parallels lat_1 and lat_2. 
    
    Parameters:
        lat_1 (float): First standard parallel (degrees)
        lat_2 (float): Second standard parallel (degrees)
        lon_0=0 (float): Longitude of map center (degrees)
        setproject=False: Use the CRS to set the project CRS
        savecrs=False: Save the custom CRS in the database 
    Returns:
        crs (QgsCoordinateReferenceSystem)
        description (str)

    
`crs_orthographic(lat, lon, setproject=False, savecrs=False)`
:   Create a custom orthographic projection centered on lat, lon. 
    
    This projections mimics the view of earth from space from infinite distance.
    Parameters:
        lat (float): Latitude (degrees)
        lon (float): Longitude (degrees)
        setproject=False: Use the CRS to set the project CRS
        savecrs=False: Save the custom CRS in the database 
    Returns:
        crs (QgsCoordinateReferenceSystem)
        description (str)

    
`crs_pacific(projection='robin', lon=-150, setproject=False, savecrs=False)`
:   Create a custom Robinson / Mollweide / Miller / Winkel Tripel etc. projection centered on a given lon. 
    
    On-the-fly reprojection of layers can result in artifacts, better to reproject the layers to this crs.
    Parameters:
        projection (str): Projection 
            use proj4 code such as: 
            'robin' (Robinson)
            'wintri' (Winkel Tripel)
            'mill' (Miller)
            'moll' (Mollweide)
            Using an invalid projection (string) raises a ValueError.
        lat (float): Latitude (degrees)
        lon (float): Longitude (degrees)
        setproject=False: Use the CRS to set the project CRS
        savecrs=False: Save the custom CRS in the database 
    Returns:
        crs (QgsCoordinateReferenceSystem)
        description (str)

    
`crs_sat(lat=40, lon=0, h=5000000, azi=0, tilt=0, setproject=False, savecrs=False)`
:   Create a custom tilted perspective projection centered on lat, lon. 
    
    This projections mimics the view of earth from a satellite in h meters altitude. 
    Nice for insets showing the area of interest. For best results, only use the upper 
    part of the resulting "globe" and eventually also rotate the map view.
    Parameters:
        lat (float): Latitude (degrees)
        lon (float): Longitude (degrees)
        h (int): altitude in meters 
        azi (float): Bearing in degrees away from north
        tilt (float): Angle in degrees away from nadir
        setproject=False: Use the CRS to set the project CRS
        savecrs=False: Save the custom CRS in the database 
    Returns:
        crs (QgsCoordinateReferenceSystem)
        description (str)

    
`cut_polygons(lon=-150, layer=None)`
:   Cut polygons for a CRS that is centered on a lon unequal 0
    
    lon: Longitude (degrees), same default as in crs_pacific()
    layer: QgsVectorLayer. Default: Use active layer.

    
`get_project_crs()`
:   Shortcut to get current project CRS. Returns: crs (QgsCoordinateReferenceSystem)

    
`save_crs(crs, description)`
:   Save a crs in the user crs database.
    
    A valid CRS that is not yet in the database will be saved to the user database
    Parameters:
        crs (QgsCoordinateReferenceSystem)
        Description (str)

    
`set_project_crs(crs)`
:   Set the project crs. Parameter: crs (QgsCoordinateReferenceSystem)

Classes
-------

`AreaOfInterest()`
:   Rectangular area of interest with methods to create matching custom CRS.
    
    Area of Interest is the extent of the active layer, or, 
    if features are selected, the bounding box of these features.
    
    Methods:
        orthographic: Return custom orthographic projection.
        sat: Return custom satellite view projection.
        laea: Return custom Lambert azimuthal equal-area projection.
        lcc: Return custom Lambert conformal conic projection.
        albers: Return custom Albers equal-area conic projection.
        save_crs: Save the crs that was created last. 
    
    Attributes:
        box: Area of Interest as QgsRectangle.
        center: Center of the Area of Interest (QgsPointXY).
        lon: Longitude of central point (float).
        lat: Latitude of central point (float).
        lat_1, lat_2: Two standard parallel enclosing 2/3 of the AOI (float).
        crs: The last CRS that was created.
        crs_desc: Description of the last CRS that was created.
        setproject: Boolean, default is True, set to false if you don't want to set the project CRS while creating a custom CRS.

    ### Methods

    `albers(self, lat_1=None, lat_2=None, lon_0=None, round_digits=None)`
    :   Create a custom Albers equal-area conic projection. 
        
        Default: Standard parallels enclose 2/3 of the area of interest and 
        lon_0 is longitude of central point of area of interest. 
        Parameters can be used to overwrite the default values.
        Parameters:
            lat_1 (float): Optional, first standard parallel (degrees)
            lat_2 (float): Optional, second standard parallel (degrees)
            lon_0 (float): Longitude of map center (degrees)
            round_digits (int): optionally round lat, lon values. 
        Returns:
            crs (QgsCoordinateReferenceSystem)

    `laea(self, lat=None, lon=None, round_digits=None)`
    :   Create a custom Lambert azimuthal equal-area projection. 
        
        Default: Centered on center of the area of interest. 
        Parameters can be used to overwrite the default values.
        Parameters:
            lat (float): Latitude of projection center (degrees)
            lon (float): Longitude of projection center (degrees)
            round_digits (int): optionally round lat, lon values. 
        Returns:
            crs (QgsCoordinateReferenceSystem)

    `lcc(self, lat_1=None, lat_2=None, lon_0=None, round_digits=None)`
    :   Create a custom Lambert conformal conic (LCC)  projection. 
        
        Default: Standard parallels enclose 2/3 of the area of interest and 
        lon_0 is longitude of central point of area of interest. 
        Parameters can be used to overwrite the default values.
        Parameters:
            lat_1 (float): Optional, first standard parallel (degrees)
            lat_2 (float): Optional, second standard parallel (degrees)
            lon_0 (float): Longitude of map center (degrees)
            round_digits (int): optionally round lat, lon values. 
        Returns:
            crs (QgsCoordinateReferenceSystem)

    `orthographic(self, lat=None, lon=None, round_digits=None)`
    :   Create a custom orthographic projection. 
        
        This projections mimics the view of earth from space from infinite distance.
        Default: Centered on center of the area of interest. 
        Parameters can be used to overwrite the default values.
        Parameters:
            lat (float): Latitude (degrees), optional.
            lon (float): Longitude (degrees), optional.
            round_digits (int): optionally round lat, lon values.  
        
        Returns:
            crs (QgsCoordinateReferenceSystem)

    `sat(self, lat=None, lon=None, h=5000000, azi=0, tilt=0, round_digits=None)`
    :   Create a custom tilted perspective projection.
        
        This projections mimics the view of earth from a satellite in h meters altitude. 
        Nice for insets showing the area of interest. For best results, only use the upper 
        part of the resulting "globe" and eventually also rotate the map view.
        Default: Centered on center of the area of interest. 
        Parameters can be used to overwrite the default values.
        Parameters:
            lat (float): Latitude (degrees), optional.
            lon (float): Longitude (degrees), optional.
            h (int): altitude in meters 
            azi (float): Bearing in degrees away from north
            tilt (float): Angle in degrees away from nadir
            round_digits (int): optionally round lat, lon values.  
        
        Returns:
            crs (QgsCoordinateReferenceSystem)

    `save_crs(self)`
    :