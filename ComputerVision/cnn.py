import tensorflow as tf
import keras
import matplotlib.pyplot as plt
import time

batch_size = 64
img_height = 48
img_width = 48
num_epochs = 150

print("Loading Datasets...")
train_ds = keras.utils.image_dataset_from_directory(
  'fer-2013\\train',
  seed=123,
  validation_split=0.2,
  subset="training",
  image_size=(img_height, img_width),
  batch_size=batch_size)

val_ds = keras.utils.image_dataset_from_directory(
  'fer-2013\\train',
  seed=123,
  validation_split=0.2,
  subset="validation",
  image_size=(img_height, img_width),
  batch_size=batch_size)

print("Found classes with names: ")
class_names = train_ds.class_names
print(class_names)

print("Building model...")
AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(500).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
print("Building model...")

data_augmentation = keras.Sequential(
  [
    keras.layers.RandomRotation(0.3),
    keras.layers.RandomZoom(0.1),
    keras.layers.RandomTranslation(height_factor=0.2, width_factor=0.2),
    keras.layers.RandomFlip(mode="horizontal"),
  ]
)

num_classes = len(class_names)
model = keras.Sequential([
  data_augmentation,
  keras.layers.Rescaling(1./255),

  keras.layers.Conv2D(64, 3, activation='relu'),
  keras.layers.MaxPooling2D(),

  keras.layers.Conv2D(128, 3, activation='relu'),
  keras.layers.MaxPooling2D(),

  keras.layers.Conv2D(256, 3, activation='relu'),
  keras.layers.MaxPooling2D(),

  keras.layers.Conv2D(512, 3, activation='relu'),
  keras.layers.MaxPooling2D(),
  keras.layers.Dropout(0.2),

  keras.layers.Flatten(),
  keras.layers.Dense(32, activation='relu'),
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
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=num_epochs
)

model.save('emotion_recognition_model_14.keras')

end = time.time()

print("Time to comile and fit model: ", (end-start), "s")


acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(num_epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()