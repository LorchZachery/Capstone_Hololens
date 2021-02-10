import os

directory = 'D:\CapstoneAI Images\cars_test'

for i in range(1, len([name for name in os.listdir(directory)]) + 1):
    if i < 10:
        os.rename(r'D:\CapstoneAI Images\cars_test\0000{}.jpg'.format(i), r'D:\CapstoneAI Images\cars_test\{}.jpg'.format(i))
    elif i < 100:
        os.rename(r'D:\CapstoneAI Images\cars_test\000{}.jpg'.format(i), r'D:\CapstoneAI Images\cars_test\{}.jpg'.format(i))
    elif i < 1000:
        os.rename(r'D:\CapstoneAI Images\cars_test\00{}.jpg'.format(i), r'D:\CapstoneAI Images\cars_test\{}.jpg'.format(i))
    elif i < 10000:
        os.rename(r'D:\CapstoneAI Images\cars_test\0{}.jpg'.format(i), r'D:\CapstoneAI Images\cars_test\{}.jpg'.format(i))
print("finished rename")