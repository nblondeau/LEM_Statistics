# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 08:58:41 2019

@author: Natali
Corresponding links:
    http://www.seanabu.com/2016/03/22/time-series-seasonal-ARIMA-model-in-python/
    https://www.datacamp.com/community/tutorials/finance-python-trading
    https://towardsdatascience.com/an-end-to-end-project-on-time-series-analysis-and-forecasting-with-python-4835e6bf050b
    
    https://www.analyticsvidhya.com/blog/2018/08/auto-arima-time-series-modeling-python-r/
    https://medium.com/@stallonejacob/time-series-forecast-a-basic-introduction-using-python-414fcb963000
    
"""
#from __future__ import print_function
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.pylab import rcParams
import os
import statsmodels.api as sm  
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
import numpy as np
from statsmodels.iolib.table import (SimpleTable, default_txt_fmt)

#Initialize some variables
Pie_Dims = (10, 10)
Bar_Dims = (10, 16)
Hist_Dims = (10,15)
LogRet_Dims = (18,14)
Series_Dims = (18,14)
HeatMap_Dims = (18, 10)
rcParams['figure.figsize'] = 15, 6
Show_Plot = False

HomeFolder = os.getcwd()
InPutFolder = HomeFolder+"/DataInPut"
OutPutFolder= HomeFolder+"/DataOutPutCurr"


#FUNCTIONS DEFINED HERE
def test_stationarity(timeseries,filename):
    
    #Determing rolling statistics
    rolmean = timeseries.rolling(12).mean()
    rolstd = timeseries.rolling(12).std()
    #Plot rolling statistics:
    fig = plt.figure(figsize=(12, 8))
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation 1y')
    plt.savefig(filename)
    plt.show()
    plt.close()
         
    #Perform Dickey-Fuller test:
    print( 'Results of Dickey-Fuller Test:')
    dftest=adfuller(timeseries,autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print (dfoutput)
    


def SARIMA(Curr_Prices_Monthly):
    # SARIMA Model Results
    # More info here https://towardsdatascience.com/an-end-to-end-project-on-time-series-analysis-and-forecasting-with-python-4835e6bf050b
    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod=sm.tsa.statespace.SARIMAX(Curr_Prices_Monthly,
                                              order=param,
                                              seasonal_order=param_seasonal,
                                              enforce_stationarity=False,
                                              enfore_invertibility=False)
                results=mod.fit()
                print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
            except:
                    continue
        
               
        
def plotMovingReturns(Curr_Prices_Monthly,Tick,Text):
    FileName = Tick+ " Rolling Mean and StdDev"+Text+'.png'
    rolmean_12 = Curr_Prices_Monthly.rolling(12).mean()    
    rolstd_12 = Curr_Prices_Monthly.rolling(12).std()
    rolmean_1 = Curr_Prices_Monthly.rolling(1).mean()    
    rolstd_1 = Curr_Prices_Monthly.rolling(1).std()        
    rolmean_3 = Curr_Prices_Monthly.rolling(3).mean()    
    rolstd_3 =  Curr_Prices_Monthly.rolling(3).std()    
    rolmean_6 = Curr_Prices_Monthly.rolling(6).mean()    
    rolstd_6 =  Curr_Prices_Monthly.rolling(6).std()    
   
    orig = plt.plot(Curr_Prices_Monthly, color='blue',label='Original')
    #mean_12 = plt.plot(rolmean_12, color='red', label='Rolling Mean 1yr')
   # std_12 = plt.plot(rolstd_12, color='black', label = 'Rolling Std 1yr')
   # mean_1 = plt.plot(rolmean_1, color='purple', label='Rolling Mean 1m')
   # std_1 = plt.plot(rolstd_1, color='green', label = 'Rolling Std 1m')
    mean_3 = plt.plot(rolmean_3, color='pink', label='Rolling Mean 3m')
    std_3 = plt.plot(rolstd_3, color='orange', label = 'Rolling Std 3m')
    #mean_6 = plt.plot(rolmean_6, color='brown', label='Rolling Mean 6m')
    #std_6 = plt.plot(rolstd_6, color='cyan', label = 'Rolling Std 6m')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation (comparing 1m,3m,6m and 1y) '+Text)
    plt.savefig(FileName)
    plt.show()
    plt.close()
    return

def plotSeasonalDecompose(Curr_Prices_Monthly,Tick,Text):
    decomposition = seasonal_decompose(Curr_Prices_Monthly, freq=12)  
    FileName = "Seasonal_decomposition_plot"+Text+'.png'
    fig = plt.figure()  
    fig = decomposition.plot()   
    fig.set_size_inches(15, 8)
    fig.suptitle('Seasonal decomposition plot (frequency 12 months'+Text)
    fig.savefig(FileName)
    fig.show()
    plt.close(fig)
    return

def plot_dicky(Curr_Prices_Monthly,Tick,Text):
    Curr_Prices_Monthly_dicky = pd.DataFrame(Curr_Prices_Monthly)
    print( 'Results of Dickey-Fuller Test: Prices '+Text)
    test_stationarity(Curr_Prices_Monthly_dicky[Tick],filename="DickyFullertest_Prices_"+Text+".png")

    print( 'Results of Dickey-Fuller Test: Log Prices'+Text)
    Curr_Prices_Monthly_dicky['log']= Curr_Prices_Monthly_dicky[Tick].apply(lambda x: np.log(x))  
    test_stationarity(Curr_Prices_Monthly_dicky['log'],filename="DickyFullertest_Log_Prices_"+Text+".png")

    print( 'Results of Dickey-Fuller Test: FirstDifference'+Text)
    Curr_Prices_Monthly_dicky['first_diff'] = (Curr_Prices_Monthly_dicky[Tick] - Curr_Prices_Monthly_dicky[Tick].shift(1))  
    test_stationarity(Curr_Prices_Monthly_dicky['first_diff'].dropna(inplace=False),filename="DickyFullertest_FirstDifference_"+Text+".png")

    print( 'Results of Dickey-Fuller Test: Log of FirstDifference'+Text)
    Curr_Prices_Monthly_dicky['first_diff_log'] = (Curr_Prices_Monthly_dicky['log'] - Curr_Prices_Monthly_dicky['log'].shift(1))  
    test_stationarity(Curr_Prices_Monthly_dicky['first_diff_log'].dropna(inplace=False),filename="DickyFullertest_Log_FirstDifference_"+Text+".png")

    print( 'Results of Dickey-Fuller Test: Seasonal Difference'+Text)
    Curr_Prices_Monthly_dicky['seasonal_diff'] =(Curr_Prices_Monthly_dicky[Tick] - Curr_Prices_Monthly_dicky[Tick].shift(12))  
    test_stationarity(Curr_Prices_Monthly_dicky['seasonal_diff'].dropna(inplace=False),filename="DickyFullertest_SeasonalDifference_"+Text+".png")

    print( 'Results of Dickey-Fuller Test: Seasonal  Log Difference'+Text)
    Curr_Prices_Monthly_dicky['log_seasonal_diff'] =(Curr_Prices_Monthly_dicky['log'] - Curr_Prices_Monthly_dicky['log'].shift(12))  
    test_stationarity(Curr_Prices_Monthly_dicky['log_seasonal_diff'].dropna(inplace=False),filename="DickyFullertest_Log_SeasonalDifference_"+Text+".png")

    print( 'Results of Dickey-Fuller Test: Seasonal  First Difference'+Text)
    Curr_Prices_Monthly_dicky['first_seasonal_diff'] =(Curr_Prices_Monthly_dicky['first_diff'] - Curr_Prices_Monthly_dicky['first_diff'].shift(12))  
    test_stationarity(Curr_Prices_Monthly_dicky['first_seasonal_diff'].dropna(inplace=False),filename="DickyFullertest_First_SeasonalDifference_"+Text+".png")

    print( 'Results of Dickey-Fuller Test: Log Seasonal  First Difference+Text')
    Curr_Prices_Monthly_dicky['log_first_seasonal_diff'] =(Curr_Prices_Monthly_dicky['first_diff_log'] - Curr_Prices_Monthly_dicky['first_diff_log'].shift(12))  
    test_stationarity(Curr_Prices_Monthly_dicky['log_first_seasonal_diff'].dropna(inplace=False),filename="DickyFullertest_Log_First_SeasonalDifference_"+Text+".png")

    #AutoCorrelation and Partial COrrelation
    FileName= "AutoCorrelation_PartialCorrelation_"+Text+'.png'
    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(211)
    fig = sm.graphics.tsa.plot_acf(Curr_Prices_Monthly_dicky['first_seasonal_diff'].iloc[13:], lags=60, ax=ax1)
    ax2 = fig.add_subplot(212)
    fig = sm.graphics.tsa.plot_pacf(Curr_Prices_Monthly_dicky['first_seasonal_diff'].iloc[13:], lags=40, ax=ax2)
    #fig.subtile('Rolling Mean & Standard Deviation (comparing 1m,3m,6m and 1y)')
    fig.savefig(FileName)
    plt.show()
    plt.close()
    return

