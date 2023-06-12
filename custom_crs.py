def crs_orthographic(lat, lon, setproject=False, savecrs=False):
    """
    Create a custom orthographic projection centered on lat, lon. 
    
    This projections mimics the view of earth from space from infinite distance.
    Parameters:
        lat (float): Latitude (degrees)
        lon (float): Longitude (degrees)
        setproject=False: Use the CRS to set the project CRS
        savecrs=False: Save the custom CRS in the database 
    Returns:
        crs (QgsCoordinateReferenceSystem)
        description (str)
    """
    proj4 = f'+proj=ortho +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0 +ellps=sphere +units=m +no_defs'
    description = f"Orthographic lat {lat}, lon {lon}"
    crs = QgsCoordinateReferenceSystem()
    crs.createFromProj4(proj4)
    if savecrs:
        save_crs(crs, description)
    if setproject:
        set_project_crs(crs)
    return crs, description


def crs_sat(lat=40, lon=0, h=5000000, azi=0, tilt=0, setproject=False, savecrs=False):
    """
    Create a custom tilted perspective projection centered on lat, lon. 
    
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
    """
    proj4 = f'+proj=tpers +lat_0={lat} +lon_0={lon} +h={h} +tilt={tilt} +azi={azi} +ellps=sphere +x_0=0 +y_0=0 +units=m'
    # proj4 = f'+proj=nsper +lat_0={lat} +lon_0={lon} +h={h} +x_0=0 +y_0=0 +units=m'
    km = int(h/1000)
    description = f"Tilted Perspective lat {lat}, lon {lon}, h {km}k, azi {azi}, tilt {tilt}"
    crs = QgsCoordinateReferenceSystem()
    crs.createFromProj4(proj4)
    if savecrs:
        save_crs(crs, description)
    if setproject:
        set_project_crs(crs)
    return crs, description


def crs_laea(lat, lon, setproject=False, savecrs=False):
    """
    Create a custom Lambert azimuthal equal-area projection centered on lat, lon. 
    
    Parameters:
        lat (float): Latitude (degrees)
        lon (float): Longitude (degrees)
        setproject=False: Use the CRS to set the project CRS
        savecrs=False: Save the custom CRS in the database 
    Returns:
        crs (QgsCoordinateReferenceSystem)
        description (str)
    """
    proj4 = f'+proj=laea +lat_0={lat} +lon_0={lon} +x_0=4321000 +y_0=3210000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs'
    description = f"LAEA centered on lat {lat}, lon {lon}"
    crs = QgsCoordinateReferenceSystem()
    crs.createFromProj4(proj4)
    if savecrs:
        save_crs(crs, description)
    if setproject:
        set_project_crs(crs)
    return crs, description   

def crs_pacific(projection='robin', lon=-150, setproject=False, savecrs=False):
    """
    Create a custom Robinson / Mollweide / Miller etc. projection centered on a given lon. 
    
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
    """
    proj4 = f'+proj={projection} +lon_0={lon} +x_0=0 +y_0=0 +datum=WGS84 +ellps=WGS84 +units=m +no_defs'
    description = f"Custom {projection} centered on lon {lon}"
    crs = QgsCoordinateReferenceSystem()
    crs.createFromProj4(proj4)
    if not crs.isValid():
        #print("Invalid CRS")
        raise ValueError("Invalid CRS")
    if savecrs:
        save_crs(crs, description)
    if setproject:
        set_project_crs(crs)
    return crs, description  


def crs_albers(lat_1, lat_2, lon_0=0, setproject=False, savecrs=False):
    """
    Create a custom Albers equal-area conic projection with standard parallels lat_1 and lat_2. 
    
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
    """
    proj4 = f'+proj=aea +lon_0={lon_0} +lat_1={lat_1} +lat_2={lat_2} +x_0=0 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs'
    description = f"Albers w. parallels {lat_1}, {lat_2}, centered lon {lon_0}"
    crs = QgsCoordinateReferenceSystem()
    crs.createFromProj4(proj4)
    if savecrs:
        save_crs(crs, description)
    if setproject:
        set_project_crs(crs)
    return crs, description   
  
    
def set_project_crs(crs):
    """Set the project crs. Parameter: crs (QgsCoordinateReferenceSystem)"""
    if crs.isValid():
        QgsProject.instance().setCrs(crs)
        print("Project CRS has been changed")
    else:
        print("Invalid CRS")
        
def save_crs(crs, description):
    """
    Save a crs in the user crs database.
    
    A valid CRS that is not yet in the database will be saved to the user database
    Parameters:
        crs (QgsCoordinateReferenceSystem)
        Description (str)
    """
    if not crs.isValid():
        print("Invalid CRS")
    elif crs.findMatchingProj():
        print("CRS already in Database")
    else:
        success = crs.saveAsUserCrs(description)
        if success:
            print("Succesfully saved CRS")
        else:
            print("Could not save CRS")

def get_project_crs():
    """Shortcut to get project CRS"""
    return QgsProject.instance().crs()