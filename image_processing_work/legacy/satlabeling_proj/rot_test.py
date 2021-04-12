import gdal
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy import ndimage, misc

#1
dataset= gdal.Open("IMG_0111_1.tif", gdal.GA_Update)

band = dataset.GetRasterBand(1)

array = band.ReadAsArray()

print(array)
#rotated = np.rot90(array, k=1)
#rotated = ndimage.rotate(array,359,reshape=False)
padded = np.pad(array, [(0,300),(0,300)], 'constant', constant_values=(0))
row_del = np.delete(padded, 0,0)
final_del = np.delete(row_del,0,1)
print(final_del)

cmap ='viridis'
plt.figure(figsize=(10,10))
plt.imshow(final_del,cmap=cmap)
plt.show()
complete = Image.fromarray(final_del)
complete.save("test_1.tif")
sr = dataset.GetProjection()
gt = dataset.GetGeoTransform()
del dataset
dataset = gdal.Open("test_1.tif", gdal.GA_Update)
dataset.SetProjection(sr)
dataset.SetGeoTransform(gt)
print(gdal.Info("test_1.tif"))
del dataset



#3
dataset= gdal.Open("IMG_0111_3.tif", gdal.GA_Update)

band = dataset.GetRasterBand(1)

array = band.ReadAsArray()

print(array)
#rotated = np.rot90(array, k=1)
#rotated = ndimage.rotate(array,359,reshape=False)
padded = np.pad(array, [(0,3000),(0,3000)], 'constant', constant_values=(0))
row_del = np.delete(padded, 0,0)
final_del = np.delete(row_del,0,1)
print(final_del)

cmap ='viridis'
plt.figure(figsize=(10,10))
plt.imshow(final_del,cmap=cmap)
plt.show()
complete = Image.fromarray(final_del)
complete.save("test_3.tif")
sr = dataset.GetProjection()
gt = dataset.GetGeoTransform()
del dataset
dataset = gdal.Open("test_3.tif", gdal.GA_Update)
dataset.SetProjection(sr)
dataset.SetGeoTransform(gt)
print(gdal.Info("test_3.tif"))
del dataset