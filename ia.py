# ===========================
# Configuração (ANTES de qualquer import do TensorFlow)
# ===========================

import os
import warnings
import logging

# Oculta mensagens do backend C++ do TensorFlow
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["ABSL_MIN_LOG_LEVEL"] = "2"

# Oculta warnings do Python
warnings.filterwarnings("ignore")

# ===========================
# Imports
# ===========================

import tensorflow as tf

# Oculta logs do TensorFlow em Python
logging.getLogger("tensorflow").setLevel(logging.ERROR)

import tf_keras as keras
from tf_keras.models import load_model

from PIL import Image, ImageOps
import numpy as np

def reciclar(caminho: str, modelo: str = "converted_keras\\keras_model.h5", classes: str = "converted_keras\\labels.txt"):

  # Disable scientific notation for clarity
  np.set_printoptions(suppress=True)

  # Load the model
  model = load_model(modelo, compile=False)

  # Load the labels
  class_names = open(classes, "r").readlines()

  # Create the array of the right shape to feed into the keras model
  # The 'length' or number of images you can put into the array is
  # determined by the first position in the shape tuple, in this case 1
  data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

  # Replace this with the path to your image
  image = Image.open(caminho).convert("RGB")

  # resizing the image to be at least 224x224 and then cropping from the center
  size = (224, 224)
  image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

  # turn the image into a numpy array
  image_array = np.asarray(image)

  # Normalize the image
  normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

  # Load the image into the array
  data[0] = normalized_image_array

  # Predicts the model | Processamento do modelo
  prediction = model.predict(data, verbose=0)#Para não mostrar aquela barra feia
  index = np.argmax(prediction)
  class_name = class_names[index]
  confidence_score = prediction[0][index]

  # Print prediction and confidence score

  print(f"Chance de ser {class_name[2:-1]}: {confidence_score * 100:.2f}%")#Medida 0 - 100
  print("-x-x-x-x-x-x-x-x-x-x-x-x-x-")

  deletar(caminho)
  if confidence_score * 100 > 80:
    return class_name[2:-1], dica(class_name[2:-1])

  else:
    return "Lixo não reconhecido", "Tente denovo"

#-x-x-x-x-x-x-x-x-x-x-x-x-

import random

dicas = {
    "garrafa": [
        "Reuse como vasos para plantas",
        "Dê para seu cachorro como brinquedo"
    ],
    
    "sacola": [
        "Reutilize para fazer compras",
        "Use para guardar objetos"
    ],
    
    "papel": [
        "Use o verso para rascunhos",
        "Recicle em pontos de coleta"
    ],
    
    "isopor": [
        "Reutilize para proteger objetos frágeis",
        "Leve para pontos de coleta de materiais recicláveis"
    ]
}

def dica(lixo):
  return dicas[lixo][random.randint(0, len(dicas[lixo])-1)]

#-x-x-x-x-x-x-x-x-x-x-x-x-
from pathlib import Path

def deletar(img):
  # Define o caminho do arquivo
  arquivo = Path(img)

  # Deleta o arquivo
  arquivo.unlink()