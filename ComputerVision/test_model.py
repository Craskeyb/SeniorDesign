import keras

model = keras.models.load_model('emotion_recognition_model.keras')
model.summary()