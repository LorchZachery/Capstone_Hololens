#def smalldir:
import os, shutil
original_train_dir = 'F:\CapstoneAI Images\cars_train'
original_test_dir = 'F:\CapstoneAI Images\cars_test'

base_dir = 'F:\CapstoneAI big'
os.mkdir(base_dir)

train_dir = os.path.join(base_dir, 'train')
os.mkdir(train_dir)
val_dir = os.path.join(base_dir, 'validation')
os.mkdir(val_dir)
test_dir = os.path.join(base_dir, 'test')
os.mkdir(test_dir)

fnames = ['{}.jpg'.format(i) for i in range(1,6108)]
for fname in fnames:
    src = os.path.join(original_train_dir, fname)
    dst = os.path.join(train_dir, fname)
    shutil.copyfile(src, dst)

fnames = ['{}.jpg'.format(i) for i in range(6109, 8144)]
for fname in fnames:
    src = os.path.join(original_train_dir, fname)
    dst = os.path.join(val_dir, fname)
    shutil.copyfile(src, dst)

fnames = ['{}.jpg'.format(i) for i in range(1,8041)]
for fname in fnames:
    src = os.path.join(original_test_dir, fname)
    dst = os.path.join(test_dir, fname)
    shutil.copyfile(src, dst)






#def initiate:
 #   from keras.applications import VGG16
  #  conv_base = VGG16(weights='imagenet', include_top = False, input_shape=(150, 150, 3))