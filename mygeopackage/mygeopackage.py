"""Main module."""
#from osgeo import ogr, osr, gdal
#import rasterio
#from rasterio.crs import CRS
#from rasterio.transform import Affine
import json

def test():
    print("mygeopackage installed!")

def array2Raster(newRasterfn, rasterOrigin, pixelWidth, pixelHeight, array, epsg=3826):
    """"Convert a numpy array to a georeferenced raster
    newRasterfn: File name for output raster
    rasterOrigin: GDAL transformation matrix for the original raster
    pixelWidth: Width of the pixels
    pixelHeight: Height of the pixels
    epsg: The spatial reference for output raster. Default is 3826.
    array: Numpy array that contains the raster cells.
    """
    cols = array.shape[1]
    rows = array.shape[0]
    originX = rasterOrigin[0]
    originY = rasterOrigin[1]
"""
    transform = rasterio.transform.from_origin(originX,originY,pixelWidth,pixelHeight)

    with rasterio.open(
        newRasterfn,
        'w',
        driver='GTiff',
        height=rows,
        width=cols,
        count=1,
        dtype=rasterio.ubyte,
        crs=CRS.from_epsg(epsg),
        transform=transform
    ) as dst:
        dst.write(array,1)
"""
"""
    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn,cols,rows,1,gdal.GDT_Float32)
    outRaster.SetGeoTransform((originX,pixelWidth,0,originY,0,pixelHeight))
    outBand = outRaster.GetRasterBand(1)
    outBand.WriteArray(array)

    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(epsg)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    
    outBand.FlushCache()
"""
def geojson2shp(fili,filo):
    with open(fili) as f:
        geojson = json.load(f)
        for feature in geojson['FeatureCollection']['features']:
            pass