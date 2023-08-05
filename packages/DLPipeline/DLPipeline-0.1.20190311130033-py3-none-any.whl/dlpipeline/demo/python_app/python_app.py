import tensorflow as tf
from keras_preprocessing.image import img_to_array, load_img
from tensorflow.python.keras.backend import clear_session
from tensorflow.python.saved_model import tag_constants

from dlpipeline.classifier.tf_classifier import TFClassifier


def prepare_img_size(img_path, sizes=(299, 299)):
  img = load_img(img_path, target_size=(sizes[0], sizes[1]))  # this is a PIL image
  x = img_to_array(img)  # this is a Numpy array with shape (3, 256, 256)
  x = x.reshape((1,) + x.shape) / 255
  return x


def run_models(session,img_path, labels_path):
  labels = []

  with open(labels_path, 'r') as f:
    for label in f.readlines():
      labels.append(label)

  image_in = prepare_img_size(img_path, sizes=(224,224))
  category_result = TFClassifier.predict(session, model_graph=graph, input_tensor=image_in)
  dlp_predictions = {k:v for v, k in zip(category_result, labels)}

  return dlp_predictions


if __name__ == '__main__':
  path_b = '/home/heider/Models/RetinaLyze/1548947081.191625/'
  exported_model_path = path_b+'export'
  img_path= '/home/heider/Pictures/retinaly_app.png'
  labels_path=path_b+'output_labels.txt'

  graph = tf.Graph()
  sess = tf.Session(graph=graph)
  tf.saved_model.loader.load(sess, [tag_constants.SERVING], exported_model_path)

  res = run_models(sess, img_path, labels_path)
  print(res)