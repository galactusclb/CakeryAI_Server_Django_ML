
import logging
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
import json

logger = logging.getLogger(__name__)

def getPredict(reportURL, modelURL,needPrediction,months = 1):
    try:
        # url = "https://cakery-ai-s3.s3-ap-southeast-1.amazonaws.com/CakeMonthlySaleReport.csv"
        url = reportURL
        df = pd.read_csv(url)

        df = df[['Month', needPrediction]]

        # load trained model
        # model = keras.models.load_model("keras.h5")
        model = keras.models.load_model("dd.h5")
        # model.summary()

        scaler = MinMaxScaler(feature_range=(0,1))

        new_df = df.filter([needPrediction])

        month = df.filter(['Month'])

        last_12Month = new_df[-60:].values
        months = month[-60:].values

        # just use 
        scaled_data = scaler.fit_transform(last_12Month)

        last_12Month_scaled = scaler.transform(last_12Month)
        X_test = []

        X_test.append(last_12Month_scaled)

        X_test = np.array(X_test)

        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        pred_sales = model.predict(X_test)

        pred_sales = scaler.inverse_transform(pred_sales)

        print(pred_sales)
        return pred_sales
    
    except FileNotFoundError:
        print("File not found")
        raise FileNotFoundError("CSV file not found")

    except (ImportError,IOError) as e:
        print("trained model not found")
        data = {"Error":"No trained model was found", "message":"You should train your activated sales report once again."}
        print(type(data))
        raise ImportError(json.dumps(data))

    except Exception as error:
        print("got error : ")
        raise Exception(error)

   
