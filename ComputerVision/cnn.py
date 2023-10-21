import tensorflow as tf
import keras
import matplotlib.pyplot as plt
import time

batch_size = 32
img_height = 180
img_width = 180

print("Loading Datasets...")
train_ds = keras.utils.image_dataset_from_directory(
  'fer-2013\\train',
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

val_ds = keras.utils.image_dataset_from_directory(
  'fer-2013\\test',
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

print("Found classes with names: ")
class_names = train_ds.class_names
print(class_names)


print("Building model...")
num_classes = len(class_names)
model = keras.Sequential([
  keras.layers.Rescaling(1./255),
  keras.layers.Conv2D(32, 3, activation='relu'),
  keras.layers.MaxPooling2D(),
  keras.layers.Conv2D(32, 3, activation='relu'),
  keras.layers.MaxPooling2D(),
  keras.layers.Conv2D(32, 3, activation='relu'),
  keras.layers.MaxPooling2D(),
  keras.layers.Flatten(),
  keras.layers.Dense(128, activation='relu'),
  keras.layers.Dense(num_classes)
])

start = time.time()

print("Compiling model...")
model.compile(
  optimizer='adam',
  loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
  metrics=['accuracy']
)

print("Fitting model...")
model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=3
)

model.save('emotion_recognition_model.keras')

end = time.time()

print("Time to comile and fit model: ", (end-start), "s")