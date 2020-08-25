# Author: Zachery J Lorch, USAFA
import os
from osgeo import gdal
from osgeo import gdalconst
import numpy as np
import matplotlib.pyplot as plt
from skimage import exposure
from app.azure_connect import Azure_Upload

class image_render:
    """
    The image_render object will render different types of bands of an image 
    for the .tif image formate

    """
    
    def __init__(self, fname, normal_size=True):
        # print(gdal.__version__)
        # opens the whole file
        if normal_size:
            # opening .tif file up to read it and extract bands
            ds = gdal.Open(fname)
            self.data = ds.ReadAsArray()
        # opens a section of the file
        else:
            # TODO: have each section of the file open up for viewing
            self.data = self.tiff_read(fname,0, 600, 0, 600)
            self.write_tiff(fname,0, 600, 0, 600)
        
        
    def tiff_read(self,fname: str, x1: int, x2: int, y1: int, y2: int, bands: list=[]) -> np.ndarray:
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


    
    def write_tiff(self, ref_file,  x1: int, x2: int, y1: int, y2: int):
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
        
        if self.data.dtype in type_info:
            predictor, gdal_type = type_info[self.data.dtype]
        else:
            raise ValueError("Arrays of type %s are not supported." % self.data.dtype)
    
        nbands, nx, ny = self.data.shape
        
    
        gtiff_flags = [ 'COMPRESS=ZSTD', # also LZW and DEFLATE works well
                        'ZSTD_LEVEL=9', # should be between 1-22, and 22 is highest compression.
                                        # 9 is default and gets essentially the same compression-rate
                    'PREDICTOR=%d' % predictor, # default is 1, use 2 for ints, and 3 for floats
                    'TILED=YES' # so that we can read sub-arrays efficiently
                    ]
        
        
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
    
        
        dir_name = "app/static/uploads"
        name = ref_file.split('/')[6].split('.')[0] + '_sectioned.tif'
        tiff_file = os.path.join(dir_name, name)
        
        
        outDrv = gdal.GetDriverByName('GTiff')
        out = outDrv.Create(tiff_file, ny, nx, nbands, gdal_type,  gtiff_flags )
        out.SetProjection(proj)
        out.SetGeoTransform(new_geotransform)
        for i in range(nbands):
            tmp = self.data[i,:,:]
            out.GetRasterBand(i+1).WriteArray(tmp)
        out.FlushCache()
        del out
        del ds
        azure_upload = Azure_Upload("imagebands/section_tiffs")
        azure_upload.upload_file(tiff_file, name)
        os.remove(tiff_file)
    
    
    
    
    
    
    
    
    def show(self,cmap='viridis'):
        """
            Shows the image with pil for debuging
        """
        plt.figure(figsize=(10,10))
        plt.imshow(self.img,cmap=cmap)
        plt.show()

    def contrast_enhance_band(self,x, percentile=(0.5, 99.5), gamma=0.5):
        """
            Gamma stretching and percentile stretching for more natural looking images.
        """
        plow, phigh = np.percentile(x, percentile)
        x = exposure.rescale_intensity(x, in_range=(plow, phigh))
        y = (x - x.min()) / (x.max()-x.min())
        y = y ** gamma
        img = (y*255).astype(np.uint8)
        return(img)
    
    def raw_rgb(self):
        # extract rgb bands
        tmp = self.data[3:0:-1,:,:] / self.data.max()
        # convert to 0-255 range
        self.img = np.transpose((255. * tmp), (1,2,0)).astype(np.uint8)
    
    def s2_to_rgb(self,rgb=[3,2,1]):
        r, g, b = rgb
        nb, nx, ny = self.data.shape
        img = np.zeros((nx, ny, 3), dtype = np.uint8)
        img[:,:,0] =  self.contrast_enhance_band(self.data[r, :, :], percentile=(0.5, 99.5), gamma=0.7)
        img[:,:,1] =  self.contrast_enhance_band(self.data[g, :, :], percentile=(0.5, 99.5), gamma=0.7)
        img[:,:,2] =  self.contrast_enhance_band(self.data[b, :, :], percentile=(0.5, 99.5), gamma=0.7)
        self.img = img
        return img
        
    def band(self, band_num):
        if band_num is None:
            return False
        if (band_num < self.data.shape[0]):
            self.img = self.contrast_enhance_band(self.data[band_num,:,:], percentile=(0.5,99.5),gamma=0.7)
            return self.img
        else: 
            # raise Exception("Band Selection is outside of range")
            return False