from image_render import image_render
from PIL import Image
import os

filename = "../test_data/IMG_0111_1.tif"
filepath = os.getcwd()  + ".jpg"

image = image_render(filename,True)
rend_image = image.s2_to_rgb()
complete_image = Image.fromarray(rend_image)
complete_image.save(filepath)

