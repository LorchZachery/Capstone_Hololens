"# CapstoneAI" 
This code will take images from yolo_visdrone/Unaccessed_Images, parse out GPS coordinates for the four corners of the image and then send the image to an AI which will look for vehicles.
For this to work, the image must have GPS data for the center coordinate, as well as the altitude the image was taken at.

To run the code, simply run python main.py in 