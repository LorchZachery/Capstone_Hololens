from keras.preprocessing.image import ImageDataGenerator
import os

base_dir = 'D:\CapstoneAI small'
train_dir = os.path.join(base_dir, 'train')
#os.mkdir(train_dir)
val_dir = os.path.join(base_dir, 'validation')

train_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(train_dir, target_size=(150, 150), batch_size = 20, class_mode='binary')

val_generator = test_datagen.flow_from_directory(val_dir, target_size=(150, 150), batch_size=20, class_mode='binary')

for data_batch, labels_batch in train_generator:
    print('data batch shape:', data_batch.shape)
    print('labels batch shape:', labels_batch.shape)
    break
    