# -*- coding: utf-8 -*-
"""Inception_resnet-15ep

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10HXYWHsYmFixGNO8iBgN2dvuDuD73Y3P
"""

# IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES
# TO THE CORRECT LOCATION (/kaggle/input) IN YOUR NOTEBOOK,
# THEN FEEL FREE TO DELETE THIS CELL.
# NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON
# ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR
# NOTEBOOK.

import os
import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from urllib.error import HTTPError
from zipfile import ZipFile
import tarfile
import shutil

CHUNK_SIZE = 40960
DATA_SOURCE_MAPPING = 'kermany2018:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F17839%2F23942%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240511%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240511T104343Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D965a96b03c81417e9d5a5653709f238932a489fb8ac795d7fcad12c94da7f331d9343752f6d69dbd674d7097ad99402d5c62c68a6501ed9427ebc6ecee38d9345b1315b4259977d356c63ee498cb6528cad07e56cc8bcdc750885a2edd04c25c0096efaf1e4e8df4b1797490bfc4b1376bdbfd86fd3227aa6090ce8e4d3ca870c267fba3e639e37de64ae4b7b9d500389c9a472b845f1280990ea4d93d3f3522a52b725aecd040547bd60830e7a44b287b362865c3bc33f061db3c683873f06e49d349d9ecc51a3bedd1e9013b0dbfb89f36feca9cdc187ee79a14029339103f704ea44777b3a096d5a15db62595f9e86f6304bfa06400a2f89b3cea8f1994cf'

KAGGLE_INPUT_PATH='/kaggle/input'
KAGGLE_WORKING_PATH='/kaggle/working'
KAGGLE_SYMLINK='kaggle'

!umount /kaggle/input/ 2> /dev/null
shutil.rmtree('/kaggle/input', ignore_errors=True)
os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)
os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)

try:
  os.symlink(KAGGLE_INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
except FileExistsError:
  pass
try:
  os.symlink(KAGGLE_WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
except FileExistsError:
  pass

for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
    directory, download_url_encoded = data_source_mapping.split(':')
    download_url = unquote(download_url_encoded)
    filename = urlparse(download_url).path
    destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)
    try:
        with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
            total_length = fileres.headers['content-length']
            print(f'Downloading {directory}, {total_length} bytes compressed')
            dl = 0
            data = fileres.read(CHUNK_SIZE)
            while len(data) > 0:
                dl += len(data)
                tfile.write(data)
                done = int(50 * dl / int(total_length))
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
                sys.stdout.flush()
                data = fileres.read(CHUNK_SIZE)
            if filename.endswith('.zip'):
              with ZipFile(tfile) as zfile:
                zfile.extractall(destination_path)
            else:
              with tarfile.open(tfile.name) as tarfile:
                tarfile.extractall(destination_path)
            print(f'\nDownloaded and uncompressed: {directory}')
    except HTTPError as e:
        print(f'Failed to load (likely expired) {download_url} to path {destination_path}')
        continue
    except OSError as e:
        print(f'Failed to load {download_url} to path {destination_path}')
        continue

print('Data source import complete.')

from tensorflow.keras.layers import Input, Lambda, Dense, Flatten,Conv2D
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications import InceptionResNetV2
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
import cv2
import os
import glob
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16
from keras.layers import Activation,Dense, Dropout, Flatten, Conv2D, ReLU
from keras.models import Model
from keras.applications.inception_v3 import InceptionV3
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
from keras.optimizers import SGD, Adam
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, precision_recall_curve, f1_score
from tensorflow.keras.utils import plot_model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from sklearn.model_selection import train_test_split
import itertools
# re-size all the images to this
IMAGE_SIZE = [224, 224]

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, MaxPooling2D, Dropout, Activation
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

total = 83484

count_cnv = 37205
count_dme = 11348
count_drusen = 8616
count_normal = 26315

cnv_weight = (1/count_cnv) * (total/4)
dme_weight = (1/count_dme) * (total/4)
drusen_weight = (1/count_drusen) * (total/4)
norm_weight = (1/count_normal) * (total/4)

class_weight = {0 : cnv_weight, 1: dme_weight, 2 : drusen_weight, 3: norm_weight}
print(class_weight)


labels = ['CNV', 'DME', 'DRUSEN', 'NORMAL']

training_data_processor = ImageDataGenerator(rescale=1./255,fill_mode='nearest')

test_data_processor = ImageDataGenerator(rescale = 1./255,fill_mode='nearest')

train_path = '/kaggle/input/kermany2018/OCT2017 /train'
test_path = '/kaggle/input/kermany2018/OCT2017 /test'
val_path = '/kaggle/input/kermany2018/OCT2017 /val'

# Load data into Python
training_data = training_data_processor.flow_from_directory(
    train_path,
    target_size = (224, 224),
    batch_size = 32,
    class_mode = 'categorical')

testing_data = test_data_processor.flow_from_directory(
    test_path,
    target_size = (224 ,224),
    batch_size = 32,
    class_mode = 'categorical',
    shuffle = False)

# Define InceptionResNetV2 model with pre-trained ImageNet weights
inception_resnet = InceptionResNetV2(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

# Freeze the weights of the pre-trained layers
for layer in inception_resnet.layers:
    layer.trainable = False

x = Flatten()(inception_resnet.output)
x = Dense(1024, activation='relu')(x)
prediction = Dense(units=4, activation='softmax')(x)

# create a model object

ir_model = Model(inputs=inception_resnet.input, outputs=prediction)
# view the structure of the model

ir_model.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)

opt = Adam(learning_rate=0.0001)
ir_model.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)
early_stop = EarlyStopping(monitor='val_loss', patience=5, verbose=1, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, verbose=1, min_lr=1e-7)

history7 = ir_model.fit(
    training_data,
    steps_per_epoch=327,
    epochs=15,
    validation_data=testing_data,
    callbacks=[early_stop, reduce_lr])

ir_model.save('ir_model.h5')

test1_loss, test1_accuracy = ir_model.evaluate(testing_data)

