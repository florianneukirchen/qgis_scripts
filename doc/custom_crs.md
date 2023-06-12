Module custom_crs
=================

Functions
---------

    
`crs_albers(lat_1, lat_2, lon_0=0, setproject=False, savecrs=False)`
:   Create a custom Albers equal-area conic projection with standard parallels lat_1 and lat_2. 
    
    The greatest accuracy is obtained if the selected standard parallels enclose two-thirds the height of the map.
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
:   Create a custom Robinson / Mollweide / Miller etc. projection centered on a given lon. 
    
    On-the-fly reprojection of layers can result in artifacts, better to reproject the layers to this crs.
    Parameters:
        projection (str): Projection 
            use proj4 code such as: 
            'robin' (Robinson)
            'mill' (Miller)
            'moll' (Mollweide)
            Using an invalid projection raises a ValueError.
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

    
`get_project_crs()`
:   Shortcut to get project CRS

    
`save_crs(crs, description)`
:   Save a crs in the user crs database.
    
    A valid CRS that is not yet in the database will be saved to the user database
    Parameters:
        crs (QgsCoordinateReferenceSystem)
        Description (str)

    
`set_project_crs(crs)`
:   Set the project crs. Parameter: crs (QgsCoordinateReferenceSystem)