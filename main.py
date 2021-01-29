import os, shutil
from keras import layers, models
from keras.preprocessing.image import ImageDataGenerator

original_train_dir = 'F:\CapstoneAI Images\cars_train'
original_test_dir = 'F:\CapstoneAI Images\cars_test'

base_dir = 'F:\CapstoneAI small'
#os.mkdir(base_dir)

train_dir = os.path.join(base_dir, 'train')
#os.mkdir(train_dir)
val_dir = os.path.join(base_dir, 'validation')
#os.mkdir(val_dir)
test_dir = os.path.join(base_dir, 'test')
#os.mkdir(test_dir)

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape = (150, 150, 3)))

model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Flatten())
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model. summary()


from keras import optimizers

model.compile(loss='binary_crossentropy', optimizer=optimizers.RMSprop(lr=1e-4),metrics=['acc']) 

trainDatagen = ImageDataGenerator(rescale=1./255)
testDatagen = ImageDataGenerator(rescale=1./255)

trainGenerator = trainDatagen.flow_from_directory(
												train_dir,
												target_size=(150, 150),
												batch_size=20,
												class_mode='binary')

valGenerator = testDatagen.flow_from_directory(
												val_dir,
												target_size=(150,150),
												batch_size=20,
												class_mode='binary')

for data_batch, labels_batch in trainGenerator:
	print('data batch shape:', data_batch.shape)
	print('labels batch shape:', labels_batch.shape)
	break
	
history = model.fit_generator(
							trainGenerator,
							steps_per_epoch=50,
							epochs=30,
							validation_data=valGenerator,
							validation_steps=25)
							
model.save('smol_car.h5')

import matplotlib.pyplot as plt

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()


