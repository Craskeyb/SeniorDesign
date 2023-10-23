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
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

val_ds = keras.utils.image_dataset_from_directory(
  'fer-2013\\test',
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

print("Found classes with names: ")
class_names = train_ds.class_names
print(class_names)


plt.figure(figsize=(10, 10))
for images, labels in train_ds.take(2):
  for i in range(9):
    ax = plt.subplot(3, 3, i + 1)
    plt.imshow(images[i].numpy().astype("uint8"))
    plt.title(class_names[labels[i]])
    plt.axis("off")
plt.show()


# print("Building model...")
# num_classes = len(class_names)
# model = keras.Sequential([
#   keras.layers.Rescaling(1./255),
#   keras.layers.Conv2D(32, 3, activation='relu'),
#   keras.layers.MaxPooling2D(),
#   keras.layers.Conv2D(32, 3, activation='relu'),
#   keras.layers.MaxPooling2D(),
#   keras.layers.Conv2D(32, 3, activation='relu'),
#   keras.layers.MaxPooling2D(),
#   keras.layers.Flatten(),
#   keras.layers.Dense(128, activation='relu'),
#   keras.layers.Dense(num_classes)
# ])

# start = time.time()

# print("Compiling model...")
# model.compile(
#   optimizer='adam',
#   loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
#   metrics=['accuracy']
# )

# print("Fitting model...")
# model.fit(
#   train_ds,
#   validation_data=val_ds,
#   epochs=3
# )

# model.save('emotion_recognition_model.keras')

# end = time.time()

# print("Time to comile and fit model: ", (end-start), "s")