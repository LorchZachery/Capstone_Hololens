# Author: Zachery J Lorch, USAFA
import os
from osgeo import gdal
from osgeo import gdalconst

import numpy as np
import matplotlib.pyplot as plt
from skimage import exposure


  
def tiff_read(fname: str, x1: int, x2: int, y1: int, y2: int, bands: list=[]) -> np.ndarray:
        """
        Reads a sub-section of the tiff array.  This call 
        > x = tiff_read(fname, i1, i2, j1, j2)
        is equivalent to
        > # read the full image
        > x = x[i1:i2, j1:j2, ...]
        except of course that the first call is much faster and more memory efficient.
        """
        
        ds = gdal.Open(fname)
        if ds is None:
            raise(FileNotFoundError("<%s> exists, but failed to open" % fname))
        ny = ds.RasterXSize
        nx = ds.RasterYSize
        if x2>nx or y2>ny or x1<0 or y1<0 or y2<y1 or x2<x1:
            raise ValueError("Invalid subset [%d:%d, %d:%d] from [0:%d, 0:%d], <%s>"
                            % (x1, x2, y1, y2, nx, ny, fname))
        if len(bands)>0:
            band = ds.GetRasterBand(1+bands[0])
            x: np.ndarray = band.ReadAsArray(y1,x1,y2-y1,x2-x1)
            array: np.ndarray = np.zeros((len(bands),x2-x1,y2-y1), dtype=x.dtype)
            array[0,:,:] = x
            for i, b in enumerate(bands):
                if i>0:
                    band = ds.GetRasterBand(b+1)
                    x: np.ndarray = band.ReadAsArray(y1,x1,y2-y1,x2-x1)
                    array[i,:,:] = x
        else:
            array: np.ndarray = ds.ReadAsArray(y1,x1,y2-y1,x2-x1)
        return array
        
def write_tiff(s2_arr, ref_file,  x1: int, x2: int, y1: int, y2: int, format_str: str, verbose=True):
    """
    obj.write_tiff('/mnt/sar-vision-data/space-eye/predictions/quincy', format_str='fake_s2_%s.tif', predictions=True)
    will write to files name
    
    """
   type_info = { np.dtype(np.float32): (3, gdalconst.GDT_Float32),
                  np.dtype(np.float64): (3, gdalconst.GDT_Float64),
                  np.dtype(np.int16): (2, gdalconst.GDT_Int16),
                  np.dtype(np.int32): (2, gdalconst.GDT_Int32),
                  np.dtype(np.uint16): (2, gdalconst.GDT_UInt16),
                  np.dtype(np.uint32): (2, gdalconst.GDT_UInt32),
                  np.dtype(np.uint8): (1, gdalconst.GDT_Byte),
                  np.dtype(np.bool): (1, gdalconst.GDT_Byte) }
    
    if s2_arr.dtype in type_info:
        predictor, gdal_type = type_info[s2_arr.dtype]
    else:
        raise ValueError("Arrays of type %s are not supported." % s2_arr.dtype)

    nbands, nx, ny = s2_arr.shape
    

    gtiff_flags = [ 'COMPRESS=ZSTD', # also LZW and DEFLATE works well
                    'ZSTD_LEVEL=9', # should be between 1-22, and 22 is highest compression.
                                    # 9 is default and gets essentially the same compression-rate
                   'PREDICTOR=%d' % predictor, # default is 1, use 2 for ints, and 3 for floats
                   'TILED=YES' # so that we can read sub-arrays efficiently
                  ]
     
    if not os.path.exists(ref_file):
        raise(FileNotFoundError("<%s> doesn't exist" % ref_file))
    ds = gdal.Open(ref_file)
    assert(ds is not None)
    # calculate the new geotransform
    geotransform = ds.GetGeoTransform()
    proj = ds.GetProjection()
    assert(proj is not None)
    orig_x, dx_x, dx_y, orig_y, dy_x, dy_y = geotransform
    assert(dx_y==0 and dy_x==0)
    x = min(x1, x2)
    y = min(y1, y2)
    orig_x += dx_x * x
    orig_y += dy_y * y
    new_geotransform = (orig_x, dx_x, dx_y, orig_y, dy_x, dy_y)

    
    
    tiff_file = os.path.join(dir_name, format_str)
    if verbose:
        print(tiff_file)
    outDrv = gdal.GetDriverByName('GTiff')
    out = outDrv.Create(tiff_file, ny, nx, nbands, gdal_type,  gtiff_flags )
    out.SetProjection(proj)
    out.SetGeoTransform(new_geotransform)
    for i in range(nbands):
        tmp = s2_arr[i,:,:]
        out.GetRasterBand(i+1).WriteArray(tmp)
    out.FlushCache()
    del out
    del ds

if __name__ =="__main__":
    real = tiff_read('static/uploads/test.tif',0,1000,0,1000)
    write_tiff('static/uploads', s2_arr=real, ref_file='static/uploads/test.tif', x1=0, x2=1000,y1=0,y2=1000 )
    
    
    
    
    
    