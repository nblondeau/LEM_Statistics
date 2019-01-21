import sys
import os

from lib import Descriptive
from lib import TimeSeries
import Initialize
import numpy as np
import itertools
import pandas as pd
import matplotlib.pylab as plt
import statsmodels.api as sm  
import datetime

HomeFolder = os.getcwd()
print(HomeFolder)

#Function to get prices from Bloomerg and to define the subset of curencies for which descriptive will run
def run_uploadprice():
   Dataset = "Small" 
   FX_Prices=Initialize.main(Dataset)
   return FX_Prices

#Function to calculating rolling mean and correlations daily
def run_descriptive_Daily(FX_Prices,HomeFolder):
   OutPutFolder= HomeFolder+"/DataOutPut"
   os.chdir(OutPutFolder)
   Start = '1-1-2017'
   End = '12-31-2018'
   ReturnFrequency = 'D' 
   Days_in_Trading_Year = 252
   Days_in_Calendar_Year = 365
   
  # T, C , ReturnFrequencyText = dd.getreturnperiod (ReturnFrequency)
   WindowDays = 91
   WindowYears = np.round(WindowDays /Days_in_Calendar_Year, decimals=2) 
   print("Processing Price Data:", Start, End, ReturnFrequency)
   Descriptive.PriceStats(FX_Prices.copy(), "FX", Start, End, ReturnFrequency, HomeFolder)
   Descriptive.RollingStats(FX_Prices.copy(), "FX", Start, End, ReturnFrequency,WindowYears,HomeFolder)

#Function to calculating rolling mean and correlations weekly
def run_descriptive_Weekly(FX_Prices,HomeFolder):
   
   Start = '1-1-2008'
   End = '12-31-2018'
   ReturnFrequency = 'W-WED' 
   Days_in_Trading_Year = 252
   Days_in_Calendar_Year = 365
   
  # T, C , ReturnFrequencyText = dd.getreturnperiod (ReturnFrequency)
   WindowDays = 180
   WindowYears = np.round(WindowDays /Days_in_Calendar_Year, decimals=2) 
   print("Processing Price Data:", Start, End, ReturnFrequency)
   Descriptive.PriceStats(FX_Prices.copy(), "FX", Start, End, ReturnFrequency)
   #Descriptive.RollingStats(FX_Prices.copy(), "FX", Start, End, ReturnFrequency,WindowYears)

# Function to basically output the rolling mean/std dev + to check seasonality plot
def run_timeseries(FX_Prices,HomeFolder):
    # set the currency for which you wnat to run the analysis
    #more details: http://www.seanabu.com/2016/03/22/time-series-seasonal-ARIMA-model-in-python/

    OutPutFolder= HomeFolder+"/DataOutCurr"
    os.chdir(OutPutFolder)
    # SPecify the currency for which you wnat to run a timeseries analysis
    Tick='MXN'
    StartDate = datetime.datetime(2009,1,9)
    EndDate = datetime.datetime(2019,1,9)

    Curr_Prices_All = pd.DataFrame(FX_Prices[Tick]).copy()
    Curr_Prices = Curr_Prices_All[StartDate:EndDate]
    Curr_Prices_clean=Descriptive.CleanDataFrame(Curr_Prices)
    Curr_DailyReturns=Descriptive.getreturns(Curr_Prices)
    
    # Resample to Monthly Returns to make it easier to plot the prices against the moving returns
    Curr_Prices_Monthly = Curr_Prices[Tick].resample('MS').mean()
    Curr_DailyReturns_Monthly= Curr_DailyReturns[Tick].resample('MS').mean()
    # Plot the DailyPrices_MovingReturns 1m, 3m, 6m, 9m, 12m and respecitive moving StandardDeviations
    print("Rolling Mean and StdDev using monthly rebased prices")
    TimeSeries.plotMovingReturns(Curr_Prices_Monthly,Tick,"Monthly Prices")
    print("Rolling Mean and StdDev using montly rebased returns")
    TimeSeries.plotMovingReturns(Curr_DailyReturns_Monthly,Tick,"Monthly Returns")  
    
    # Plot Seasonal Decomposition plot
    # more details: http://www.seanabu.com/2016/03/22/time-series-seasonal-ARIMA-model-in-python/
    print("Seasonal Decomposition Plot on Prices (Frequency 12 months)")
    TimeSeries.plotSeasonalDecompose(Curr_Prices_Monthly,Tick,"Using Monthly Prices")
    print("Seasonal Decomposition Plot on Returns (Frequency 12 months)")
    TimeSeries.plotSeasonalDecompose(Curr_DailyReturns_Monthly,Tick,"Using Returns")

    return Curr_Prices_Monthly, Curr_Prices_clean,Curr_DailyReturns, Curr_DailyReturns_Monthly, Tick

def run_DickyFuller_Prices(Curr_Prices_Monthly,Tick,HomeFolder):
    #more detais: http://www.seanabu.com/2016/03/22/time-series-seasonal-ARIMA-model-in-python/
    # Plot the stationarity for differnet inputs     
    
    OutPutFolder= HomeFolder+"/DataOutCurr"
    os.chdir(OutPutFolder)
    TimeSeries.plot_dicky(Curr_Prices_Monthly,Tick,"Prices")

def run_DickyFuller_Returns(Curr_DailyReturns_Monthly,Tick,HomeFolder):
    #more detais: http://www.seanabu.com/2016/03/22/time-series-seasonal-ARIMA-model-in-python/
    # Plot the stationarity for differnet inputs     
    
    OutPutFolder= HomeFolder+"/DataOutCurr"
    os.chdir(OutPutFolder)
    TimeSeries.plot_dicky(Curr_DailyReturns_Monthly,Tick,"Returns")

def run_SARIMA(Curr_Prices_Monthly,HomeFolder):
    # SARIMA Model Results
    # More info here https://towardsdatascience.com/an-end-to-end-project-on-time-series-analysis-and-forecasting-with-python-4835e6bf050b
    # Check which output suggests the lowest AIC and use that order/seasonal order below
    OutPutFolder= HomeFolder+"/DataOutCurr"
    os.chdir(OutPutFolder)
    mod = sm.tsa.statespace.SARIMAX(Curr_Prices_Monthly, order=(1, 1, 1), 
                                    seasonal_order=(1, 1, 0, 12), enforce_stationarity=False,
                                    enforce_invertibility=False)
    results = mod.fit()
    FileName= "SARIMA"+'.png'
    print (results.summary())
    results.plot_diagnostics(figsize=(16, 8))
    plt.savefig(FileName)
    plt.show()
    plt.close()


if __name__ == '__main__':
    FX_Prices=run_uploadprice()
    #run_descriptive_Daily(FX_Prices,HomeFolder)
    Curr_Prices_Monthly, Curr_Prices_clean,Curr_DailyReturns, Curr_DailyReturns_Monthly,Tick=run_timeseries(FX_Prices,HomeFolder)
    run_DickyFuller_Prices(Curr_Prices_Monthly,Tick,HomeFolder)
    #run_DickyFuller_Returns(Curr_DailyReturns_Monthly,Tick,HomeFolder)
    run_SARIMA(Curr_Prices_Monthly,HomeFolder)