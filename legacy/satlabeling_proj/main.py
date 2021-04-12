from image_render import image_render
from PIL import Image
import os
import sys
import rasterio
import rasterio.plot
import pyproj
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


filename = "bgrnet.tiff"
filepath = "stack.tif"

image = image_render(filename,True)
rend_image = image.band(6)
image.show()

#complete_image = Image.fromarray(rend_image)
#complete_image.save(filepath)

"""
gdal_merge.py -separate -o out.tif -v  -ot Int16  ../test_data/IMG_0200_4.tif ../test_data/IMG_0200_2.tif ../test_data/IMG_0200_3.tif ../test_data/IMG_0200_1.tif ../test_data/IMG_0200_5.tif

"""
"""
https://www.earthdatascience.org/courses/use-data-open-source-python/multispectral-remote-sensing/landsat-in-Python
"""