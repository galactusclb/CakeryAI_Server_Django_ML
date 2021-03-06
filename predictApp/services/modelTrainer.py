
import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense,LSTM
import matplotlib.pyplot as plt
import pickle
import os

import time
# from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings as django_settings

# get current time in milliseconds
def current_milli_time():
    return round(time.time() * 1000)
  

def trainModel(url, product, userId):
  try:
    plt.style.use('fivethirtyeight')

    needPrediction = product

    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    # url = "https://cakery-ai-s3.s3-ap-southeast-1.amazonaws.com/CakeMonthlySaleReport.csv"

    df = pd.read_csv(url)
    print(df.head())

    df.shape

    #Create a new dataframe with only the 'Close colums'
    data = df.filter([needPrediction])
    #Convert the dataframe to a numpy array
    dataset = data.values
    # dataset

    #Get the number of rows to train the model on
    training_data_len = math.ceil( len(dataset) * .8 )

    # print()
    training_data_len

    # scale the data
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)

    # scaled_data

    # Crate the scaled training data set
    train_data = scaled_data[0:training_data_len, :]
    # Split the data into x_train and y_train data sets
    x_train = []
    y_train = []

    for i in range(60, len(train_data)):
      x_train.append(train_data[i-60:i,0])
      y_train.append(train_data[i,0])
      if i<=61:
        print(x_train)
        print(y_train)
        print()

    # Convert the x_train and y_train to numpy arrays
    x_train,y_train = np.array(x_train), np.array(y_train)

    #Reshape the data
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_train.shape

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True,input_shape = (x_train.shape[1] , 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')


    # Train the model
    model.fit(x_train, y_train, batch_size=1, epochs=10)

    # modelSavePath = os.path.join(dir_path,'pre_trained_models/keras_'+str(current_milli_time())+'.h5')
    modelSavePath = os.path.join(django_settings.STATIC_ROOT, 'pre_trained_models/keras_'+str(current_milli_time())+'.h5')
    print(modelSavePath)
    model.save(modelSavePath)

    # val_loss, val_acc = model.evaluate(x_train, y_train)
    # print(val_loss, val_acc)

    # load trained model
    loadedModel = keras.models.load_model(modelSavePath)
    loadedModel.summary()

    # Create the testing data set
    # Create a new array containing scaled values from index x to x
    test_data = scaled_data[training_data_len - 60:, :]
    # ?Create the data sets x_test and y_test
    x_test = []
    y_test = dataset[training_data_len:, :]

    for i in range(60, len(test_data)):
      x_test.append(test_data[i-60:i, 0])

    # Convert the data to a numpy array
    x_test = np.array(x_test)

    # Reshape the data 
    x_test = np.reshape( x_test, (x_test.shape[0],x_test.shape[1],1 ))

    # get the models predicted price values
    predictions = model.predict(x_test)
    # print(predictions)

    # for testing
    before_inverce_predictions = predictions

    predictions = scaler.inverse_transform(predictions)
    # predictions

    # get the root mean squared error ( RMSE )
    rmse = np.sqrt( np.mean(predictions - y_test)**2 )
    # rmse

    # Plot the data 
    train = data[: training_data_len]
    valid = data[training_data_len: ]
    valid['Predictions'] = predictions
    valid['before_inverce_predictions'] = before_inverce_predictions

    #show the valid and predicted prices
    print(modelSavePath)
    return modelSavePath

  except FileNotFoundError:
        print("File not found")
        raise FileNotFoundError("CSV file not found")    

  except Exception as error:
        print("got error : ")
        raise Exception(error)