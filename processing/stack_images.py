import os, glob
import micasense.capture as capture
import cv2
import numpy as np
import matplotlib.pyplot as plt
import micasense.imageutils as imageutils
import micasense.plotutils as plotutils


# # This is an older RedEdge image without RigRelatives
# imagePath = os.path.join(os.path.abspath('.'),'data','0000SET','000')
# imageNames = glob.glob(os.path.join(imagePath,'IMG_0001_*.tif'))
# panelNames = glob.glob(os.path.join(imagePath,'IMG_0000_*.tif'))

# # Image from the example RedEdge imageSet (see the ImageSet notebook) without RigRelatives.
# imagePath = os.path.expanduser(os.path.join('~','Downloads','RedEdgeImageSet','0000SET'))
# imageNames = glob.glob(os.path.join(imagePath,'000','IMG_0013_*.tif'))
# panelNames = glob.glob(os.path.join(imagePath,'000','IMG_0000_*.tif'))

directory = 'stacked'
def stackImages(FILE, imageNames, panelNames=None):
    import os, glob
    import micasense.capture as capture
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    import micasense.imageutils as imageutils
    import micasense.plotutils as plotutils
    # Allow this code to align both radiance and reflectance images; bu excluding
    # a definition for panelNames above, radiance images will be used
    # For panel images, efforts will be made to automatically extract the panel information
    # but if the panel/firmware is before Altum 1.3.5, RedEdge 5.1.7 the panel reflectance
    # will need to be set in the panel_reflectance_by_band variable.
    # Note: radiance images will not be used to properly create NDVI/NDRE images below.
    if panelNames is not None:
        panelCap = capture.Capture.from_filelist(panelNames)
    else:
        panelCap = None
    
    capture = capture.Capture.from_filelist(imageNames)
    
    if panelCap is not None:
        if panelCap.panel_albedo() is not None:
            panel_reflectance_by_band = panelCap.panel_albedo()
        else:
            panel_reflectance_by_band = [0.67, 0.69, 0.68, 0.61, 0.67] #RedEdge band_index order
        panel_irradiance = panelCap.panel_irradiance(panel_reflectance_by_band)    
        img_type = "reflectance"
        capture.plot_undistorted_reflectance(panel_irradiance)
    else:
        if capture.dls_present():
            img_type='reflectance'
            #capture.plot_undistorted_reflectance(capture.dls_irradiance())
        else:
            img_type = "radiance"
            #capture.plot_undistorted_radiance()
    

    
    ## Alignment settings
    match_index = 1 # Index of the band 
    max_alignment_iterations = 10
    warp_mode = cv2.MOTION_HOMOGRAPHY # MOTION_HOMOGRAPHY or MOTION_AFFINE. For Altum images only use HOMOGRAPHY
    pyramid_levels = 0 # for images with RigRelatives, setting this to 0 or 1 may improve alignment
    
    
    print("Aligning images. Depending on settings this can take from a few seconds to many minutes")
    # Can potentially increase max_iterations for better results, but longer runtimes
    warp_matrices, alignment_pairs = imageutils.align_capture(capture,
                                                            ref_index = match_index,
                                                            max_iterations = max_alignment_iterations,
                                                            warp_mode = warp_mode,
                                                            pyramid_levels = pyramid_levels)
    if warp_matrices == -1:
        return -1
    print("Finished Aligning, warp matrices={}".format(warp_matrices))
    
    cropped_dimensions, edges = imageutils.find_crop_bounds(capture, warp_matrices, warp_mode=warp_mode)
    im_aligned = imageutils.aligned_capture(capture, warp_matrices, warp_mode, cropped_dimensions, match_index, img_type=img_type)
    
    # Create a normalized stack for viewing
    im_display = np.zeros((im_aligned.shape[0],im_aligned.shape[1],im_aligned.shape[2]), dtype=np.float32 )
    
    
    
    from osgeo import gdal, gdal_array
    rows, cols, bands = im_display.shape
    driver = gdal.GetDriverByName('GTiff')
    filename = FILE + "stacked"  #blue,green,red,nir,redEdge
    filename = os.path.join(directory,filename)
    outRaster = driver.Create(filename+".tiff", cols, rows, im_aligned.shape[2], gdal.GDT_UInt16)
    
    normalize = (img_type == 'radiance') # normalize radiance images to fit with in UInt16
    
    # Output a 'stack' in the same band order as RedEdge/Alutm
    # Blue,Green,Red,NIR,RedEdge[,Thermal]
    # reflectance stacks are output with 32768=100% reflectance to provide some overhead for specular reflections
    # radiance stacks are output with 65535=100% radiance to provide some overhead for specular reflections
    
    # NOTE: NIR and RedEdge are not in wavelength order!
    
    multispec_min = np.min(im_aligned[:,:,1:5])
    multispec_max = np.max(im_aligned[:,:,1:5])
    
    for i in range(0,5):
        outband = outRaster.GetRasterBand(i+1)
        if normalize:
            outdata = imageutils.normalize(im_aligned[:,:,i],multispec_min,multispec_max)
        else:
            outdata = im_aligned[:,:,i]
            outdata[outdata<0] = 0
            outdata[outdata>2] = 2
        
        outdata = outdata*32767
        outdata[outdata<0] = 0
        outdata[outdata>65535] = 65535
        outband.WriteArray(outdata)
        outband.FlushCache()
    
    if im_aligned.shape[2] == 6:
        outband = outRaster.GetRasterBand(6)
        outdata = im_aligned[:,:,5] * 100 # scale to centi-C to fit into uint16
        outdata[outdata<0] = 0
        outdata[outdata>65535] = 65535
        outband.WriteArray(outdata)
        outband.FlushCache()
    outRaster = None
    return 1


