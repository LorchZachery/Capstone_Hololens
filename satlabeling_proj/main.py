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


filename = "out.tif"
filepath = "../test_data/IMG_0111_1.tif"
# The grid of raster values can be accessed as a numpy array and plotted:
with rasterio.open(filepath) as src:
    oviews = src.overviews(1)
    print(oviews)
"""
image = image_render(filename,True)
rend_image = image.raw_rgb()
image.show()

complete_image = Image.fromarray(rend_image)
complete_image.save(filepath)
"""
"""
gdal_merge.py -separate -o out.tif -v  -ot Int16  ../test_data/IMG_0111_4.tif ../test_data/IMG_0111_2.tif ../test_data/IMG_0111_3.tif ../test_data/IMG_0111_1.tif ../test_data/IMG_0111_5.ti

"""
https://www.earthdatascience.org/courses/use-data-open-source-python/multispectral-remote-sensing/landsat-in-Python/