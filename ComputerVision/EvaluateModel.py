import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import keras 
import seaborn
import sklearn.metrics as met

model = tf.keras.models.load_model('emotion_recognition_model_5.keras')
# class_names =  ['angry', 'fear', 'happy', 'neutral', 'sad', 'surprise']
class_names =  ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
tf.keras.utils.plot_model(model, to_file='model.png', show_shapes=True)

test_ds = keras.utils.image_dataset_from_directory(
  'fer-2013\\test',
  labels="inferred",
  shuffle=False,
  label_mode="int", 
  image_size=(48, 48))

test_labels = np.concatenate([y for _,y in test_ds], axis=0).tolist()

type_counts = [test_labels.count(i) for i in range(len(class_names))]
for i, c in enumerate(type_counts):
  print("Found", c, "files belonging to", class_names[i], ".")

results = model.predict(test_ds)
result_labels = [np.argmax(i) for i in results]

cf = tf.math.confusion_matrix(test_labels, result_labels).numpy()

correct = 0
for i in range(len(test_labels)):
  if test_labels[i] == result_labels[i]:
    correct += 1

print(correct/len(test_labels))

print(met.classification_report(test_labels, result_labels, target_names=class_names))


cm = met.confusion_matrix(test_labels, result_labels)
cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]



plt.figure('Normalized')
seaborn.heatmap(cm_norm, annot=True, fmt='.2f', cmap='cividis')
plt.xlabel("Prediction")
plt.ylabel("Actual")
plt.xticks([i+0.5 for i in range(len(class_names))], class_names)
plt.yticks([i+0.5 for i in range(len(class_names))], class_names, rotation=45)
plt.title("Normalized Confusion Matrix")
# plt.show()

plt.figure('Raw')
seaborn.heatmap(cm, annot=True, fmt='d', cmap='cividis')
plt.xlabel("Prediction")
plt.ylabel("Actual")
plt.xticks([i+0.5 for i in range(len(class_names))], class_names)
plt.yticks([i+0.5 for i in range(len(class_names))], class_names, rotation=45)
plt.title("Confusion Matrix")
plt.show()


