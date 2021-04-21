
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 10,6
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf,pacf
from statsmodels.tsa.arima_model import ARIMA
from datetime import datetime


def test_stationarity(timeseires):

    # determing rolling statistics
    movingAverage = timeseires.rolling(window=12).mean()
    movingSTD = timeseires.rolling(window=12).std()

    #plot rolling statistics
    orig = plt.plot(timeseires, color='blue',   label='Original')
    mean = plt.plot(movingAverage, color='red',   label='Rolling Mean')
    std = plt.plot(movingSTD, color='black',   label='Rolling std')
    plt.legend(loc="best")
    plt.title("Rlling mean & std")
    # plt.show(block=False)

    # perform dickey-fluller test:
    print("Result of Dickey-Fuller Test:")
    dftest = adfuller(timeseires['Sales'], autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test statics', 'p-values', '#Lags Used', ' Number of Observations used'])

    for key,value in dftest[4].items():
        dfoutput['Critical Values (%s)'%key] = value

    # print(dfoutput)



def getPredict(months = 1):
    url = "https://cakery-ai-s3.s3-ap-southeast-1.amazonaws.com/CakeMonthlySaleReport.csv"
    dataset = pd.read_csv(url)

    # dataset = pd.read_csv('d:/SLIIT/3rd yr - UOB/2nd Sem/Research 2nd sem/py/CakeMonthlySaleReport.csv')
    dataset['Month'] = pd.to_datetime(dataset['Month'], infer_datetime_format=True)
    indexedDataset = dataset.set_index(['Month'])

    # 
    print(indexedDataset.head(5))



    plt.xlabel('Date')
    plt.ylabel('Number of sales')
    # plt.plot(indexedDataset)

    rolmean = indexedDataset.rolling(window=12).mean()

    rolstd = indexedDataset.rolling(window=12).std()

    print(rolmean, rolstd)

    print('sas')

    orig = plt.plot(indexedDataset, color='blue',   label='Original')
    mean = plt.plot(rolmean, color='red',   label='Rolling Mean')
    std = plt.plot(rolstd, color='green',   label='Rolling std')
    plt.legend(loc="best")
    plt.title("Rlling mean & std")
    # plt.show(block=False)


    print('Result of Dickey-fuller test:')
    dftest = adfuller(indexedDataset['Sales'], autolag='AIC')

    dfoutput = pd.Series(dftest[0:4], index=['Test statics', 'p-values', '#Lags Used', ' Number of Observations used'])

    # for key,value in dftest[4].items():
    # dfoutput['Critical Values (%s)'%key] = value

    print(dfoutput)

    indexedDataset_logScale = np.log(indexedDataset)

    # plt.plot(indexedDataset_logScale)

    movingAverage = indexedDataset_logScale.rolling(window=12).mean()

    movingStd = indexedDataset_logScale.rolling(window=12).std()

    # plt.plot(indexedDataset_logScale)
    # plt.plot(movingAverage, color="red")

    datasetLogScaleMinusMovingAverage = indexedDataset_logScale - movingAverage
    datasetLogScaleMinusMovingAverage.head(12)

    # remove nun  Values
    datasetLogScaleMinusMovingAverage.dropna(inplace=True)
    datasetLogScaleMinusMovingAverage.head(10)



    # test_stationarity(datasetLogScaleMinusMovingAverage)

    exponentialDecayWeightAvg = indexedDataset_logScale.ewm(halflife=12, min_periods=0, adjust=True).mean()
    # plt.plot(indexedDataset_logScale)
    # plt.plot(exponentialDecayWeightAvg, color="red")

    datasetLogScaleMinusMovingExponentialDecayAvg = indexedDataset_logScale - exponentialDecayWeightAvg
    # test_stationarity(datasetLogScaleMinusMovingExponentialDecayAvg)

    datasetLogDiffShifting = indexedDataset_logScale - indexedDataset_logScale.shift()
    # plt.plot(datasetLogDiffShifting)

    datasetLogDiffShifting.dropna(inplace=True)
    # test_stationarity(datasetLogDiffShifting)


    decomposition = seasonal_decompose(indexedDataset_logScale)

    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid

    # plt.subplot(411)
    # plt.plot(indexedDataset_logScale, label="Original")
    # plt.legend(loc="best")
    # plt.subplot(412)
    # plt.plot(trend, label="Trend")
    # plt.legend(loc="best")
    # plt.subplot(413)
    # plt.plot(seasonal, label="Seasonality")
    # plt.legend(loc="best")
    # plt.subplot(414)
    # plt.plot(residual, label="Residuals")
    # plt.legend(loc="best")
    # plt.tight_layout()

    decomposedLogdata = residual
    decomposedLogdata.dropna(inplace=True)

    # test_stationarity(decomposedLogdata)

    decomposedLogdata = residual
    decomposedLogdata.dropna(inplace=True)
    # test_stationarity(decomposedLogdata)

    # ACf & PACF plots:


    lag_acf = acf(datasetLogDiffShifting, nlags=20)
    lag_pacf = pacf(datasetLogDiffShifting, nlags=20, method='ols')

    # plot ACF:
    # plt.subplot(121)
    # plt.plot(lag_acf)
    # plt.axhline(y=0,linestyle='--', color="gray")
    # plt.axhline(y=-1.96/np.sqrt(len(datasetLogDiffShifting)), linestyle="--", color="gray")
    # plt.axhline(y=1.96/np.sqrt(len(datasetLogDiffShifting)), linestyle="--", color="gray")
    # plt.title("Autocorrection function")

    # plot PACF:
    # plt.subplot(122)
    # plt.plot(lag_pacf)
    # plt.axhline(y=0,linestyle='--', color="gray")
    # plt.axhline(y=-1.96/np.sqrt(len(datasetLogDiffShifting)), linestyle="--", color="gray")
    # plt.axhline(y=1.96/np.sqrt(len(datasetLogDiffShifting)), linestyle="--", color="gray")
    # plt.title("Partial Autocorrection function")
    # plt.tight_layout()



    # AR model
    model = ARIMA(indexedDataset_logScale, order=(2,1,2))
    results_AR = model.fit(disp=-1)
    # plt.plot(datasetLogDiffShifting)
    # plt.plot(results_AR.fittedvalues, color="red")
    # plt.title("RSS: %.4f"% sum((results_AR.fittedvalues - datasetLogDiffShifting['Sales'])**2))
    print('Plotting AR model')

    #MA model
    model = ARIMA(indexedDataset_logScale, order=(0,1,2))
    results_MA = model.fit(disp=-1)
    # plt.plot(datasetLogDiffShifting)
    # plt.plot(results_MA.fittedvalues, color='red')
    # plt.title('RSS: %.4f'% sum((results_MA.fittedvalues - datasetLogDiffShifting['Sales'])**2))
    print('Plotting MA model')

    model = ARIMA(indexedDataset_logScale, order=(2,1,2))
    results_ARIMA = model.fit(disp=-1)
    # plt.plot(datasetLogDiffShifting)
    # plt.plot(results_ARIMA.fittedvalues, color='red')
    # plt.title('RSS: %.4f'% sum((results_ARIMA.fittedvalues - datasetLogDiffShifting['Sales'])**2))

    predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
    print(predictions_ARIMA_diff)

    # convert to cumlative sum
    predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
    print(predictions_ARIMA_diff_cumsum)

    predictions_ARIMA_log = pd.Series(indexedDataset_logScale['Sales'].iloc[0], index = indexedDataset_logScale.index)
    predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum, fill_value=0)
    predictions_ARIMA_log

    predictions_ARIMA = np.exp(predictions_ARIMA_log)
    # plt.plot(indexedDataset)
    # plt.plot(predictions_ARIMA)

    indexedDataset_logScale

    results_ARIMA.plot_predict(1,261)

    results = results_ARIMA.forecast(steps=months)
    results

    converted_results = [(np.exp(x)) for x in [i for i in results]]
    converted_results

    # np.exp(results[0])
    pred_sales = np.exp(results[0])
    print(pred_sales)
    
    return pred_sales 

   
