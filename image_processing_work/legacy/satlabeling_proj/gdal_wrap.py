import gdal
import struct
input_file_1= "test_1.tif"
input_file_2= "../test_data/IMG_0111_2.tif"
input_file_3= "../test_data/IMG_0111_3.tif"

ds = gdal.Open(input_file_2,gdal.GA_ReadOnly)

print("driver: {}/{}".format(ds.GetDriver().ShortName,ds.GetDriver().LongName))
print("Size is {} x {} x {}".format(ds.RasterXSize,
                                                ds.RasterYSize,
                                                ds.RasterCount))
print("Projection is {}".format(ds.GetProjection()))

geotransform = ds.GetGeoTransform()
if geotransform:
    print("Origin = ({}, {})".format(geotransform[0], geotransform[3]))
    print("Pixel Size = ({}, {})".format(geotransform[1], geotransform[5]))

ulx, xres, xskew, uly, yskew, yres = ds.GetGeoTransform()
lrx = ulx + (ds.RasterXSize * xres)
lry = uly + (ds.RasterYSize * yres)

print(gdal.Info(input_file_1))


vrt_options = gdal.BuildVRTOptions(separate=True)
my_vrt = gdal.BuildVRT('my.vrt',[input_file_1, input_file_2,input_file_3], options=vrt_options) 
my_vrt = None
vrt = gdal.Open('my.vrt')
print(vrt)
gdal.Translate('stack.tif', vrt)
