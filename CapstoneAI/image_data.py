from PIL import Image
from PUL.ExifTags import TAGS

img_name = "loctets.tif"

img = Image.open(img_name)

exif = img.getexif()

for tagID 