<<<<<<< HEAD
# Capstone_Hololens
Each directory has readme  
* andriod_app holds code that runs an app that can run on an andriod. this app allows for adding bombs, delete, and can be the gps moduler if the PI zero doesn't have one.  
* image_app_processing_work holds code that can process altuim images (tifs) based on how the project is moving probably wont be as needed, yet there is a lot of good code for processing images.  
* useful_scripts holds scripts that help with a lot fo small annoying tasks. Such as communicating with database as well as get x and y from lat and lon.  
* pi_server is all the scripts that allow the pi zero to be excessable and connected to, it also includes the gps connection script
=======
# CapstoneAI - JonathanNash21

This folder holds all the important scripts for running the image parser, AI, and database update.

To run this code, simply navigate to the folder and use ```python main.py```

This program will run until interrupted by 'Ctrl-C', and will check CapstoneAI/Unaccessed_Images for any new images. New images will be parsed for GPS coordinates, and then will be sent to the AI to be checked for "bombs" (cars currently). 

In order for everything to work properly, the image must have embedded GPS and altitude data (usually done automatically depending on the camera). This information is necessary, as it allows us to calculate the GPS location of every "bomb" that was detected by the AI (accurate to about 1x10^-6) and send those coordinates to the database to be used by the HoloLens.

The AI and database updates will be done automatically after the program detects new images in the unaccessed folder - for testing purposes, there are two images, "loctets.jpeg" and "IMG_0055_3.tif" that have geolocation data but no vehicles in them, stored in CapstoneAI/geolocation_imgs. You can copy+paste these into the unaccessed folder and see how the images are parsed and what the geolocation data in the dictionary looks. 


**Important** - You need to make sure, if using these images multiple times, that the Accessed folder is empty before re-running the program. If you never restarted the program, the images will simply be deleted and not used, but if you re-run, you will receive this error:

"Traceback (most recent call last):
  File "main.py", line 115, in <module>
    asyncio.run(initial.look_for_image()) # look for images in the unaccessed folder -> init.py/look_for_image
  File "C:\ProgramData\Anaconda3\lib\asyncio\runners.py", line 43, in run
    return loop.run_until_complete(main)
  File "C:\ProgramData\Anaconda3\lib\asyncio\base_events.py", line 616, in run_until_complete
    return future.result()
  File "D:\HololensIED\CapstoneAI\init.py", line 125, in look_for_image
    os.rename(img_path, img_new) # move this image to the accessed folder
FileExistsError: [WinError 183] Cannot create a file when that file already exists: 'D:\\HololensIED\\CapstoneAI\\Unaccessed_Images\\loctets.jpeg' -> 'D:\\HololensIED\\CapstoneAI\\Accessed_Images\\loctets.jpeg'"

This is because the code moves images from the unaccessed folder to the accessed one, so if there are duplicates there and you have restarted the program, the implemented protections to prevent this error will not work. Good practice would be to empty the Accessed folder every time you perform a keyboard interrupt to stop the program - something simple to implement would be to do that automatically upon exiting the while loop (it will be an os library command, already imported) - this could be one of the first things you do if you feel it necessary to do so.

# Suggestions for first-time interactions

First, run the program using one of the images in geolocation_imgs, let it parse, and then let it sit for a bit, and then throw the other image in there. Take note of what is printed out, and then interrupt the program and try to make sense of what it is telling you. Second, comment out line 118 and uncomment line 119 in main.py, and then change self.access_path to False in init.py. You can also uncomment line 140 in main.py, this but make sure that the Pi is on and you are connected to the "Capstone" wifi (**Not "DFCS-Capstone or DFCS-Capstone_5G**). This will run our test image that has cars in it along with "GPS data". This will show you what an image with detectable data and proper GPS coordinate information should look like, and will update the database (assuming everything is on and connected correctly). The reason we had to hardcode in GPS coordinates for this image is because it is a screen shot taken off of Google Earth - we did not have access to drones reliably to be able to make our own data of, say, the cadet parking lot, so we had to spoof our own images off of Google Earth. This was for proof-of-concept purposes only, and the next team(s) should focus on getting drone data of cars or, better yet, something related to IEDs that can be used to train a new AI model. In addition to toying around with the program in this way, it is imperative that you read through each and every line of code. You should absolutely understand what main.py and init.py are doing, as these are what you will interact with the most. You should also read over obj_det_custom_yolo_live.py - this is the AI that looks through each image, and also interacts with other scripts that are used to allow for the AI to "interact" with the database. If you end up training a new AI model, this is the script that you will be replacing, so you will need to add in important pieces of code in order to be able to stay connected with every other script. These lines that **must** be integrated into a new model are lines 79, 83, and 201-210. Most of the code in obj_det_custom_yolo_live.py was written by @stevenjnovotny, a professor who (as of Spring 2021) works with the Autonomous Systems class - Dr. Mello might be able to find him if you have questions and want to talk with Dr. Novotny. I tried to comment as much of his code as I could in areas that might seem confusing, but a lot of the comments in that code are where I added in new stuff. I would suggest reading through the rest of the scripts, but they are not as important as these three and can, for the most part, be run without any interaction on your part (besides adding in the required code for any new AI created).

Once you have a good understanding of what this is doing, your efforts would be best be suited finding some way to train an AI on IED data, or finding one that is already made (very difficult, we looked early on in the semester and couldn't find anything, although our search was somewhat limited).
The most difficult part of this would be finding data that is good enough to train on, as well as having enough of that data. 

# CapstoneAI_OLD

This folder is what I was doing while reading "Deep Learning with Python" by Francois Chollet, this book was supplied by Major Wilson. It was helpful for understanding a lot of the general idea behind creating your own AI model from scratch, but ultimately did not get me very far. I kept it here for docmentation of previous work, but it is messy code and undocumented - look at it at your own risk. I gave the book back either to Major Wilson directly, or to LtCol Merritt/de Freitas for safekeeping. It is a good read, so if you have time and are building a model from scratch I would highly suggest taking a look at it.

>>>>>>> CapstoneAI/main
