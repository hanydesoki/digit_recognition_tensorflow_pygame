import tensorflow as tf

model = tf.keras.models.load_model('model_mnist.h5')

def predict(X):
    return model.predict(X.reshape(1, 28, 28, 1))