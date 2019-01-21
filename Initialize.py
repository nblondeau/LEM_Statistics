# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 09:57:11 2019

@author: Natali & Pierre
"""

import os
from lib import Descriptive as dd
import pandas as pd

def main(dataset):
   HomeFolder = os.getcwd()
   InPutFolder = HomeFolder+"/DataInPut"
   OutPutFolder= HomeFolder+"/DataOutPut"
   os.chdir(HomeFolder)
   Dataset=dataset

   FX_Sheet = "_FX_Rates.xlsx"
   FX_Tab = "FX_Rates"
   ## Factors
   Factor_Sheet = "_Factors.xlsx"
   FactorTab = "Factors"
   # BenchMark Portfolio Data
   Benchmark_Sheet = "_Benchmark.xlsx"
   BenchmarkTab = "Benchmark"
   ## Local Currency Interest Index

    ######################################################
    ##SET THE DATE RANGES OF THE TOTAL DATASET
    #StartDate=Start
    #EndDate = End
    #ReturnFrequency = 'D'  #   D, W-WED... 
   Days_in_Trading_Year = 252
   Days_in_Calendar_Year = 365
   ReturnPeriod = 5  # Use weekly Returns assuming data without weekends, ie a 5 day week
    # Calculate Log Returns?
   Log_Return = False
#
    # Generate Lists of Frequency Types in Python
   Months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
   Days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT','SUN']
   Daily = ['D', 'B', ]
   Monthly = ['M', 'BM', 'MS', 'BMS']
   Weekly =  []; Quarterly = []; Annualy = []
   W = 'W-'
   for d in Days:
       Weekly.append(W+d)
       Q0 = 'Q-' ; Q1 = 'QS-'; Q2 = 'BQ-'; Q3 = 'BQS-'
       for m in Months:
           Quarterly.append(Q0+m)
           Quarterly.append(Q1+m)
           Quarterly.append(Q2+m)
           Quarterly.append(Q3+m)
           A0 = 'A-'; A1 = 'AS-'; A2 = 'BA-'; A3 = 'BAS-'
           for m in Months:
               Annualy.append(A0+m)
               Annualy.append(A1+m)
               Annualy.append(A2+m)
               Annualy.append(A3+m)

   # Set Chart Parameters
   Pie_Dims = (10, 10)
   Bar_Dims = (10, 16)
   Hist_Dims = (10,15)
   LogRet_Dims = (18,14)
   Series_Dims = (18,14)
   HeatMap_Dims = (18, 10)
   Show_Plot = False
 
    # FACTORS TO ANNUALIZE Log Return/Var
#   ReturnFrequency= 'D'
#   T, C , ReturnFrequencyText = Data_Download.getreturnperiod (ReturnFrequency)
#   Ret_Factor =  Days_in_Trading_Year / T
#   Std_Factor = np.sqrt ( Ret_Factor )
#   Var_Factor = Ret_Factor 

    # In[]
    ##############################################################################
   os.chdir(InPutFolder)

   ALL_Factor = dd.LoadExcel (Factor_Sheet, FactorTab,  0,  3)
   ALL_FX = dd.LoadExcel (FX_Sheet,  FX_Tab,  0,  3) 
    ##%time ALL_LocCurr = LoadExcel (LocCurr_Sheet, LocCurrTab, 0, 3)
    #%time ALL_BenchMark = LoadExcel (Benchmark_Sheet, BenchmarkTab,  0, 3)

    # In[]
    # INVERT ALL FX QUOTES TO DIRECT QUOTES (ie expressed as US$, not Local Curr)
   #ALL_FX= dd.invertquote(ALL_FX) 

   # In[]
   
   ################################################################
   #     SPLIT THE DATA into Prices, Factors, BenchMarks and BenchMarkWeights
    
   # Get Money Market Index Data
   #MM_Header = ['xUSD']
   #MoneyMarket = pd.DataFrame(ALL_LocCurr[MM_Header]).copy()
    
   Factor_Headers = ['MXWD','DXY','VIX','CRB','US5YBE','US1YLibFw','USEU1YSp','USJY1YSp']
   Factor_Prices = pd.DataFrame(ALL_Factor[Factor_Headers]).copy()

   #BenchMark_Headers = ['EM22_FX','BBRG_8EM','BBRG_ASIA','BBRG_EMEA','BBRG_G10','BBRG_Latam']
   #BenchMark_Prices =  pd.DataFrame(ALL_BenchMark[BenchMark_Headers]).copy()

   # USE Large or Small Currency Datase
   if Dataset =="Large" :
       FX_Headers = ['ARS','CNH','RUB','SGD','TRY',
                     'ZAR','BRL','CLP','COP','IDR',
                     'INR','KRW','MYR','PEN','PHP',
                     'THB','TWD','MXN',
                     'EURHUF','EURCZK','EURPLN','EURRON']
       BMW1 = ['_ARS','_CNH','_CZK','_PLN','_RON','_RUB',
           '_SGD','_TRY','_ZAR','_BRL','_CLP']
       BMW2 = ['_COP','_IDR','_INR','_KRW','_MYR','_PEN',
           '_PHP','_THB','_TWD','_MXN','_HUF']
       BMW  = BMW1 + BMW2
       LCH1 = ['xARS','xCNH','xRUB','xSGD','xTRY','xZAR',
           'xBRL','xCLP','xCOP','xIDR','xINR']
       LCH2 = ['xKRW','xMYR','xPEN','xPHP','xTHB','xTWD',
           'xMXN','xHUF','xCZK','xPLN','xRON']
       LCH  = LCH1 + LCH2
   elif Dataset =="Small" :
       FX_Headers = ['TRY','BRL','MXN','ZAR','EUR','GBP']
       BMW = ['_TRY','_BRL','_MXN','_ZAR']
       LCH = ['xTRY','xBRL','xMXN','xZAR']
   else: print("DATASET ERROR.")

#    
   FX_Prices = pd.DataFrame(ALL_FX[FX_Headers]).copy()
    #LocCurrs = pd.DataFrame(ALL_LocCurr[LCH]).copy()
    #BenchMarkWeights = pd.DataFrame(ALL_BenchMark[BMW]).copy()


   
   
   
   return FX_Prices