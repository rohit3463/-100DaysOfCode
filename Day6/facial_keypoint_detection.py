# -*- coding: utf-8 -*-
"""facial-keypoint-detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jRObvIwaVrjapUfCAjiZZrTJNZVAS3LY
"""

#authenticating google drive
!pip install -U -q PyDrive

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

# 1. Authenticate and create the PyDrive client.
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

#importing files into notebook
downloaded = drive.CreateFile({'id':''})
downloaded.GetContentFile('training.csv')
downloaded = drive.CreateFile({'id':''})
downloaded.GetContentFile('test.csv')

#imporing libraries needed to load the data
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

from keras.models import load_model
from pandas.io.parsers import read_csv
from sklearn.utils import shuffle

#function to load data into numpy array and some preprocessing
def load_data(test=False):
  FTRAIN = 'training.csv'
  FTEST = 'test.csv'
  
  fname = FTEST if test else FTRAIN
  df = read_csv(fname)
  
  df['Image'] = df['Image'].apply(lambda x : np.fromstring(x, sep=" "))
  
  df = df.dropna()
  
  X = np.vstack(df['Image'].values) / 255
  X = X.astype(np.float32)
  X = X.reshape(-1, 96, 96, 1)
  
  if not test:
    y = df[df.columns[:-1]].values
    y = (y-48) / 48
    X, y = shuffle(X, y, random_state = 42)
    
  else:
    y = None
    
  return X, y

#importing necessary libraries for training the model
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Conv2D, MaxPooling2D, Dropout
from keras.layers import Flatten, Dense
from keras.optimizers import SGD, RMSprop, Adagrad, Adadelta, Adam, Adamax, Nadam


# Designing the model architecture
def get_my_CNN_model_architecture():
  
  model = Sequential()
  
  model.add(Conv2D(32, (5, 5), input_shape = (96, 96, 1), activation = 'relu'))
  model.add(MaxPooling2D(pool_size = (2, 2)))
  
  model.add(Conv2D(64, (3, 3), activation = 'relu'))
  model.add(MaxPooling2D(pool_size = (2,2)))
  model.add(Dropout(0.1))
  
  model.add(Conv2D(128, (3, 3), activation = 'relu'))
  model.add(MaxPooling2D(pool_size = (2, 2)))
  model.add(Dropout(0.2))
  
  model.add(Conv2D(30, (3, 3), activation = 'relu'))
  model.add(MaxPooling2D(pool_size = (2, 2)))
  model.add(Dropout(0.3))
  
  model.add(Flatten())
  
  model.add(Dense(64, activation = 'relu'))
  model.add(Dense(128, activation = 'relu'))
  model.add(Dense(256, activation = 'relu'))
  model.add(Dense(64, activation = 'relu'))
  model.add(Dense(30))
  
  return model

# compile the model
def compile_my_CNN_model(model, optimizer, loss, metrics):
  return model.compile(optimizer = optimizer, loss = loss, metrics = metrics)

#train the model
def train_my_CNN_model(model, X_train, y_train):
  return model.fit(X_train, y_train, epochs = 100, batch_size = 200, verbose = 1, validation_split = 0.2)

#saving the model
def save_my_CNN_model(model, filename):
  model.save(filename + '.h5')

# loading the model
def load_my_CNN_model(filename):
  return load_model(filename + '.h5')

#model into action
X_train, y_train = load_data()

my_model  = get_my_CNN_model_architecture()

compile_my_CNN_model(my_model, optimizer = 'adam', loss = 'mse', metrics = ['accuracy'])

hist = train_my_CNN_model(my_model, X_train, y_train)

save_my_CNN_model(my_model, 'my_model')