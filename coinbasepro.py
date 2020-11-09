# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 12:08:52 2020

@author: TimboSlicerr
"""


# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 11:23:50 2020

@author: TimboSlicerr
"""

# /root/thinclient_drives/Document/CBPRO

import cbpro
import requests, json, matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

from apscheduler.schedulers.background import BackgroundScheduler

import time

from datetime import datetime, timedelta
import threading
import math
import os
from pytz import timezone
import copy

key = 'api keys goes here'
b64secret = 'api secret goes here'
passphrase = 'passphrase goes here'

auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)


currencies = []
currencyHighs = {}
currencyDelta = {}
currencyAllDeltas = {}

ThresholdDeltas = {}

minuteFirst = {}
minuteDeltas = {}

fiveMinuteFirst = {}
fiveMinuteDeltas = {}

fifteenMinuteFirst = {}
fifteenMinuteDeltas = {}

hourFirst = {}

BuySellList = {}
BuySellCopy = {}

breakValue = False

global hours
global minutes
global days
global iteration
global index
global minuteBuyThresh, minuteSellThresh, fiveMinuteBuyThresh, fiveMinuteSellThresh
global fifteenMinuteBuyThresh, fifteenMinuteSellThresh, hourBuyThresh, hourSellThresh
global Sells
global Buys
global balanceList
global accountList
global emergencySells
global twentyMinuteLogDif, fiveMinuteLogDif, hourLogDif, fourHourLogDif
global twentyMinuteMomentum, fiveMinuteMomentum, hourMomentum, fourHourMomentum
global twentyMinuteStability, fiveMinuteStability, hourStability, fourHourStability
global twentyMinuteLogMax, fiveMinuteLogMax, hourLogMax, fourHourLogMax
global minLength
global TFClarksIndicator
global currencyIndex
global totalminutes
global totalprofit
global currencyIL
global sixHourMomentum, twelveHourMomentum
global buyT, sellT
global setUpBool

setUpBool = False

buyT = []
sellT = []
sixHourMomentum = {}
twelveHourMomentum = {}
threeDayMomentum = {}
sevenDayMomentum = {}
oneMonthMomentum = {}


currencyIndex = 0



fiveMinuteLogDif = {}
twentyMinuteLogDif = {}
hourLogDif = {}
fourHourLogDif = {}


fiveMinuteLogMax = {}
twentyMinuteLogMax = {}
hourLogMax = {}
fourHourLogMax ={}


fiveMinuteStability = {}
twentyMinuteStability = {}
hourStability = {}
fourHourStability = {}

fiveMinuteMomentum = {}
twentyMinuteMomentum = {}
hourMomentum = {}
fourHourMomentum = {}


accountList = {}
balanceList = {}
emergencySells = {}

minutes = 0
hours = 0
days = 0
iteration = 1

totalminutes = 0





currencyIL = ['BTC-USD', 'ETH-USD', 'XRP-USD', 'LTC-USD', 'BCH-USD', 'EOS-USD', \
              'DASH-USD', 'OXT-USD' , 'MKR-USD', 'XLM-USD', 'ATOM-USD', \
                  'XTZ-USD', 'ETC-USD', 'OMG-USD', 'LINK-USD', 'REP-USD', \
                      'ZRX-USD', 'ALGO-USD', 'DAI-USD', 'KNC-USD', 'COMP-USD', \
                          'BAND-USD', 'NMR-USD', 'CGLD-USD', 'UMA-USD', \
                              'LRC-USD', 'YFI-USD', 'UNI-USD', 'REN-USD', 'BAL-USD']
        
currencyIL = sorted(currencyIL)

def setUp():
    
    for cur in currencyIL:
        
            currencies.append(cur)
            currencyHighs[cur] = 0.00
            currencyDelta[cur] = 0.00
            minuteFirst[cur] = []
            minuteDeltas[cur] = []
            fiveMinuteFirst[cur] = []
            fiveMinuteDeltas[cur] = []
            fifteenMinuteFirst[cur] = []
            fifteenMinuteDeltas[cur] = []
            hourFirst[cur] = []
            hourDeltas[cur] = []
            currencyAllDeltas[cur] = []
            ThresholdDeltas[cur] = []
           
            emergencySells[cur] = []
            
            fiveMinuteLogDif[cur] = {}
            fiveMinuteLogDif[cur]['time'] = []
            fiveMinuteLogDif[cur]['value'] = []
            twentyMinuteLogDif[cur] = {}
            twentyMinuteLogDif[cur]['time'] = []
            twentyMinuteLogDif[cur]['value'] = []        
            hourLogDif[cur] = {}
            hourLogDif[cur]['time'] = []
            hourLogDif[cur]['value'] = []
            
            fourHourLogDif[cur] = []
            
            fiveMinuteMomentum[cur] = {}
            fiveMinuteMomentum[cur]['time'] = []
            fiveMinuteMomentum[cur]['value'] = []
            twentyMinuteMomentum[cur] = {}
            twentyMinuteMomentum[cur]['time'] = []
            twentyMinuteMomentum[cur]['value'] = []
            hourMomentum[cur] = {}
            hourMomentum[cur]['time'] = []
            hourMomentum[cur]['value'] = []
            fourHourMomentum[cur] = []
            
            
            fiveMinuteStability[cur] = {}
            fiveMinuteStability[cur]['time'] = []
            fiveMinuteStability[cur]['value'] = []
            twentyMinuteStability[cur] = {}
            twentyMinuteStability[cur]['time'] = []
            twentyMinuteStability[cur]['value'] = []
            hourStability[cur] = {}
            hourStability[cur]['time'] = []
            hourStability[cur]['value'] = []
            fourHourStability[cur] = []
            
            fiveMinuteLogMax[cur] = {}
            fiveMinuteLogMax[cur]['time'] = []
            fiveMinuteLogMax[cur]['value'] = []
            twentyMinuteLogMax[cur] = {}
            twentyMinuteLogMax[cur]['time'] = []
            twentyMinuteLogMax[cur]['value'] = []
            hourLogMax[cur] = {}
            hourLogMax[cur]['time'] = []
            hourLogMax[cur]['value'] = []
            fourHourLogMax[cur] = []
            
        
         
            
            BuySellList[cur] = {}
            BuySellList[cur]['BuyTime'] = []
            BuySellList[cur]['BuyPrice'] = []
            BuySellList[cur]['SellTime'] = []
            BuySellList[cur]['SellPrice'] = []
            BuySellList[cur]['ProfitPercentage'] = []
            BuySellList[cur]['Fees'] = []
            BuySellList[cur]['TotalMinutes'] = []
            # BuySellList[cur]['Success'] = []
        
        
            
            sixHourMomentum[cur] = []
            twelveHourMomentum[cur] = []
            threeDayMomentum[cur] = []
            sevenDayMomentum[cur] = []
            oneMonthMomentum[cur] = []
            
            
            
def setUpWithPrevData():
    
    global DataFramesPrev
    global hourFirst, hourDeltas

    
    path1 = "/root/CBPRO/prevData3"
    
    CSVFiles = [x for x in os.listdir(path1) if x.endswith(".csv")]
    
    DataFramesPrev = {}
    
    #Loading the Data
    hourFirst = {}
    
  
    for data in CSVFiles:
        curN = data.strip('.csv')
        print(curN)
        csvpath = path1 + '/' + data
        if('HourlyFirst' in csvpath or 'fiveMinuteFirst' in csvpath or 'fifteenMinuteFirst' in csvpath):
            df = pd.read_csv(csvpath, sep=r'\t')
            DataFramesPrev[curN] = df

    for dt in DataFramesPrev:
        curName = dt.split('.')[0]
        curName1 = curName + '-USD'
        
        if("HourlyFirst" in dt):
            tmpHrFirst = []
            for v in DataFramesPrev[dt].values:
                v1 = float(v)
                tmpHrFirst.append(v1)
                
            hourFirst[curName1] = tmpHrFirst
            
        if("fifteenMinuteFirst" in dt):
                tmpFirst = []
                for v in DataFramesPrev[dt].values:
                    v1 = float(v)
                    tmpFirst.append(v1)
                    
                fifteenMinuteFirst[curName1] = tmpFirst
                
        if("fiveMinuteFirst" in dt):
                tmpFirst = []
                for v in DataFramesPrev[dt].values:
                    v1 = float(v)
                    tmpFirst.append(v1)
                    
                fiveMinuteFirst[curName1] = tmpFirst
                
 
    
    for cur in currencyIL:
        
            currencies.append(cur)
            currencyHighs[cur] = 0.00
            currencyDelta[cur] = 0.00
            minuteFirst[cur] = []
            minuteDeltas[cur] = []
            fiveMinuteDeltas[cur] = []
            fifteenMinuteDeltas[cur] = []

            currencyAllDeltas[cur] = []
            ThresholdDeltas[cur] = []
           
            emergencySells[cur] = []
            
            fiveMinuteLogDif[cur] = {}
            fiveMinuteLogDif[cur]['time'] = []
            fiveMinuteLogDif[cur]['value'] = []
            twentyMinuteLogDif[cur] = {}
            twentyMinuteLogDif[cur]['time'] = []
            twentyMinuteLogDif[cur]['value'] = []        
            hourLogDif[cur] = {}
            hourLogDif[cur]['time'] = []
            hourLogDif[cur]['value'] = []
            
            fourHourLogDif[cur] = []
            
            fiveMinuteMomentum[cur] = {}
            fiveMinuteMomentum[cur]['time'] = []
            fiveMinuteMomentum[cur]['value'] = []
            twentyMinuteMomentum[cur] = {}
            twentyMinuteMomentum[cur]['time'] = []
            twentyMinuteMomentum[cur]['value'] = []
            hourMomentum[cur] = {}
            hourMomentum[cur]['time'] = []
            hourMomentum[cur]['value'] = []
            fourHourMomentum[cur] = []
            
            
            fiveMinuteStability[cur] = {}
            fiveMinuteStability[cur]['time'] = []
            fiveMinuteStability[cur]['value'] = []
            twentyMinuteStability[cur] = {}
            twentyMinuteStability[cur]['time'] = []
            twentyMinuteStability[cur]['value'] = []
            hourStability[cur] = {}
            hourStability[cur]['time'] = []
            hourStability[cur]['value'] = []
            fourHourStability[cur] = []
            
            fiveMinuteLogMax[cur] = {}
            fiveMinuteLogMax[cur]['time'] = []
            fiveMinuteLogMax[cur]['value'] = []
            twentyMinuteLogMax[cur] = {}
            twentyMinuteLogMax[cur]['time'] = []
            twentyMinuteLogMax[cur]['value'] = []
            hourLogMax[cur] = {}
            hourLogMax[cur]['time'] = []
            hourLogMax[cur]['value'] = []
            fourHourLogMax[cur] = []
            
         
            
            BuySellList[cur] = {}
            BuySellList[cur]['BuyTime'] = []
            BuySellList[cur]['BuyPrice'] = []
            BuySellList[cur]['SellTime'] = []
            BuySellList[cur]['SellPrice'] = []
            BuySellList[cur]['ProfitPercentage'] = []
            BuySellList[cur]['Fees'] = []
            BuySellList[cur]['TotalMinutes'] = []
            # BuySellList[cur]['Success'] = []
            

        
            
            sixHourMomentum[cur] = []
            twelveHourMomentum[cur] = []
            threeDayMomentum[cur] = []
            sevenDayMomentum[cur] = []
            oneMonthMomentum[cur] = []
        
        

print('Would you like to load previous Data? Enter y')
setUpInput = input()
        
print("Select Interval: Minutes, Seconds, or Hours: \nType M, S, or H then hit Enter")
intervalType = input()

print("Enter length for the Interval to Run: ")
intervalLength = float(input())

minLength = 0.00

if(intervalType == 'H'):
    print("Enter the number of Minutes:")
    minLength = float(input())
    

                
    
    


public_client = cbpro.PublicClient()       


def checkTicker(): 
   
    global currencies, currencyHighs, currencyDelta, currencyAllDeltas, sec1float, ThresholdDeltas
    global min1int, hour1int
    global minuteFirst, minuteDeltas
    global fiveMinuteFirst, fiveMinuteDeltas
    global fifteenMinuteFirst, fifteenMinuteDeltas
    global hourFirst,  hourDeltas
    global secfloat
    global minutes, hours, days
    global iteration, index
    global currencyIndex
    global tempProduct
    global tempPrice
    global totalminutes
    global currencyIL
    
    for item in range(3):
        
        tempProduct = {}
        tempPrice = 0.00
        prID = ''
        curLength = len(currencyIL)
        
    
    
    
    
    
    
        
        if(currencyIndex <= curLength-1):
            prID = currencyIL[currencyIndex]
            
        # print('Running Ticker')
        # print(curLength)
        
        if(iteration == 1):
            
            prID = 'BTC-USD'
            tempProduct = public_client.get_product_ticker(product_id=prID)
        
            tempPrice = float(tempProduct['price'])
            
        elif(iteration != 1 and currencyIndex <= curLength-1):
            # print(currencyIndex)
            # print(prID)
            if(prID == 'BTC-USD'):
                currencyIndex = currencyIndex + 1
                continue
            elif(prID != 'BTC-USD'):
                tempProduct = public_client.get_product_ticker(product_id=prID)
                tempPrice = float(tempProduct['price'])
                currencyIndex = currencyIndex + 1
                

            
        central = timezone('US/Central')
        now2 = datetime.now(central)
       
        # timenow2=now2.strftime("%H:%M:%S.%f")
        sec2 = now2.strftime('%S.%f')
        
        sec2float = float(sec2)
        
        
        curSec = sec2float - sec1float
       
        
        if(sec2float < sec1float):
            curSec = (60 - sec1float) + sec2float
            
            
        
        if(curSec > 59 and iteration == 1):
            minutes = minutes + 1
            totalminutes = totalminutes + 1
           
        
         
            
        if(minutes >= 60 and iteration == 1):
            hours = hours + 1
            minutes = 0
            
        
        if(hours >= 24 and iteration == 1):
            days = days + 1
            hours = 0
            
       
            
       
            
        # print('\n')
        # print(str(iteration) + ' - iterations')
        curSecInt = int(curSec)
        
        if(curSecInt%15 == 0 and iteration == 1 and curSecInt != 60):
            currencyIndex = 0
            
        if(days >= 1 and hours == 0 and minutes == 1 and curSecInt == 29):
            t3 = threading.Thread(target=createDataFrames())
            t3.start()
            
            
        if(iteration >= 3):
            iteration = 1
        else:
            iteration = iteration + 1
            
        
        if(prID == ''):
            print('Skipping...')
            continue
       

        print(prID)
        priceFloat = tempPrice
        print(str(priceFloat) + ' - current Price')
        print('\n')
        print(str(curSec) + ' - seconds')

        print(str(minutes) + ' - minutes')
        print(str(hours) + ' - hours')
        print(str(days) + ' - days')
        print('\n')
        
        
        
        
        
        firstIteration = True   
        
        
        if(prID == 'BTC-USD'):
        
            if(curSec >= 1):
                
                firstIteration = False  
            
            if(curSec >= 59 and iteration == 1):
                # print("\nResetting deltas\n")
                
                currencyDelta[prID] = 0.00
                currencyHighs[prID] = priceFloat
                      
          
                
            if(firstIteration == True):
                
                currencyDelta[prID] = 0.00
                
            elif(firstIteration == False):
            
                currencyDelta[prID] = (((priceFloat - currencyHighs[prID]) + .0000001)/currencyHighs[prID])*100   
           
            if(currencyDelta[prID] != 0):
                
                # print("\nDelta")
                # print(currencyDelta[prID])
                # print('\n')
                emergencyDelta = float(currencyDelta[prID])
                EmergencyDeltaCheck(emergencyDelta, prID)            
                
                
            if(curSec < 1):
                
              currencyHighs[prID] = priceFloat
              minuteFirst[prID].append(priceFloat)
    
              if(minutes == 0):
                      
                      fiveMinuteFirst[prID].append(priceFloat)
                      fifteenMinuteFirst[prID].append(priceFloat)
                      hourFirst[prID].append(priceFloat)
                      
                      
              if(minutes%5 == 0 and minutes != 0):
                      
                      fiveMinuteFirst[prID].append(priceFloat)
                      
              if(minutes%15 == 0 and minutes != 0):
                      
                      fifteenMinuteFirst[prID].append(priceFloat)
               
              if(minutes >= 1 or (hours >= 1 and minutes == 0)):
                     # tmpIndex = index - 1
                      lastPriceFloat = float(minuteFirst[prID][-2])
                      price = ((priceFloat - lastPriceFloat + .0000001)/lastPriceFloat)*100
                      minuteDeltas[prID].append(price)
                      # print('\n')
                      # print('Minute Delta: ' + str(price))
                      # print('\n')
                      
                      if(minutes%5 == 0):
                          
                          # tmpIndex = int(index/5) - 1
                          lastPriceFloat = float(fiveMinuteFirst[prID][-2])
                          price = ((priceFloat - lastPriceFloat + .0000001)/lastPriceFloat)*100
                          fiveMinuteDeltas[prID].append(price)
                          # print('\n')
                          # print('Five Minute Delta:  ' + str(price))
                          # print('\n')
                          
                          
                      if(minutes%15 == 0):
                         
                          # tmpIndex = int(index/15) - 1
                          lastPriceFloat = float(fifteenMinuteFirst[prID][-2])
                          price = ((priceFloat - lastPriceFloat + .0000001)/lastPriceFloat)*100
                          fifteenMinuteDeltas[prID].append(price)
                          # print('\n')
                          # print('Fifteen Minute Delta: ' + str(price))
                          # print('\n')
                      
                      
            if(setUpBool == False):  
                
                if(curSec < 1 and totalminutes > 1):
                    dataAnalysis(prID, minutes)
                    
                    
                if((curSec < 1 and hours >= 4) or (curSec < 1 and days >= 1)):
                    createTFClarkIndicator(prID, priceFloat)
                    
                if((curSec < 1 and hours >= 4) or (curSec < 1 and days >= 1)):
                    deltaChecks(prID, priceFloat, hours)
                    
            if(setUpBool == True):
                
                if(curSec < 1 and totalminutes > 1):
                    dataAnalysis(prID, minutes)
                    
                    
                if(curSec < 1 and totalminutes > 60):
                    createTFClarkIndicator(prID, priceFloat)
                    
                if(curSec < 1 and totalminutes > 60):
                    deltaChecks(prID, priceFloat, hours)
                      
                      
        
        if(prID != 'BTC-USD'):
                  
            if(curSec < 15):
    
                  minuteFirst[prID].append(priceFloat)
        
                  if(minutes == 0):
                      
                      fiveMinuteFirst[prID].append(priceFloat)
                      fifteenMinuteFirst[prID].append(priceFloat)
                      hourFirst[prID].append(priceFloat)
                      
                
                      
                  if(minutes%5 == 0 and minutes != 0):
                      
                      fiveMinuteFirst[prID].append(priceFloat)
                      
                  if(minutes%15 == 0 and minutes != 0):
                      
                      fifteenMinuteFirst[prID].append(priceFloat)
               
              
              # print('\nAdding Data...')
                  if(minutes >= 1 or (hours >= 1 and minutes == 0)):
                      # tmpIndex = index - 1
                        lastPriceFloat = float(minuteFirst[prID][-2])
                        price = ((priceFloat - lastPriceFloat + .0000001)/lastPriceFloat)*100
                        minuteDeltas[prID].append(price)
                        # print('\n')
                        # print('Minute Delta: ' + str(price))
                        # print('\n')
                    
                        if(minutes%5 == 0):
                    
                            # tmpIndex = int(index/5) - 1
                            lastPriceFloat = float(fiveMinuteFirst[prID][-2])
                            price = ((priceFloat - lastPriceFloat + .0000001)/lastPriceFloat)*100
                            fiveMinuteDeltas[prID].append(price)
                            # print('\n')
                            # print('Five Minute Delta:  ' + str(price))
                            # print('\n')
                
                    
                        if(minutes%15 == 0):
                       
                            # tmpIndex = int(index/15) - 1
                            lastPriceFloat = float(fifteenMinuteFirst[prID][-2])
                            price = ((priceFloat - lastPriceFloat + .0000001)/lastPriceFloat)*100
                            fifteenMinuteDeltas[prID].append(price)
                            # print('\n')
                            # print('Fifteen Minute Delta: ' + str(price))
                            # print('\n')
          
                        
                     
                        

            
            
            
            if(setUpBool == False):
            
                if(curSec < 30 and curSec > 15 and totalminutes > 1):
                    dataAnalysis(prID, minutes)
                    
                    
                if((curSec < 30 and curSec > 15 and hours >= 4) or (curSec < 30 and curSec > 15 and days >= 1)):
                    createTFClarkIndicator(prID, priceFloat)
                    
                if((curSec < 30 and curSec > 15 and hours >= 4) or (curSec < 30 and curSec > 15 and days >= 1)):
                    deltaChecks(prID, priceFloat, hours)
                    
            elif(setUpBool == True):
                
                if(curSec < 30 and curSec > 15 and totalminutes > 1):
                    dataAnalysis(prID, minutes)
                    
                    
                if(curSec < 30 and curSec > 15 and totalminutes > 60):
                    createTFClarkIndicator(prID, priceFloat)
                    
                if(curSec < 30 and curSec > 15 and totalminutes > 60):
                    deltaChecks(prID, priceFloat, hours)
       
            
def sellOrder(prID):
    
    global sellT
    print('Placing a Sell Order!!!')
    tmpID = prID.split('-')[0]
    balance = float(balanceList[tmpID])
    balanceR = int(balance*1000)/1000


    S = auth_client.place_market_order(product_id=prID,side='sell', size = balanceR)
    sellT.append(S)
    
    updateBalance()
    
    
def buyOrder(prID):
    
    global buyT
    print('Placing a Buy Order!!!')
    funds = float(balanceList['USD'])
    
    if(funds >= 500):
        B = auth_client.place_market_order(product_id=prID,side='buy', funds='500.00')
        buyT.append(B)
    elif(funds < 500):
        print('Not Enough Funds')
        
    updateBalance()
        
        
def EmergencyDeltaCheck(delta, prID):
    
    global balanceList
    global sellT
    print('\nEmergency Check:')
    print(delta)
    print('\n')
    curID = prID.split('-')[0]
    balance = balanceList[curID]
    
    if(delta < -5):
        print("Sell Everything!!!!!")
        for acct in balanceList:
            balance = float(balanceList[acct])
            balanceR = int(balance*1000)/1000
            if(balance > 0 and acct != 'USD'):
                print('Selling ' + str(balance) + ' of ' + str(acct))
                ESID = acct + '-USD'
                sellT = auth_client.place_market_order(product_id=ESID, side='sell', size = balanceR)
                now = datetime.now()
                emergencyTime = now.strftime("%H:%M:%S.%f")
                emergencySells[ESID].append(emergencyTime)
                
        updateBalance()
        


def deltaChecks(cur, priceFloat, hours):
    global Buys, Sells
    
    central = timezone('US/Central')
    now = datetime.now(central)
    actionTime = now.strftime("%D-%H:%M")
    
    
    # Add custom algorithms here to decide whether to buy or sell
    # Use buyOrder and sellOrder if certain conditions are met based on algorithm
    
    print('\nChecking ' + cur + ' for buy and sell Threshold... \n')




def createTFClarkIndicator(prID, price):
    
  print('TFCLARK Indicator')
    
        
        
def dataAnalysis(prID, minutes):
    
      global twentyMinuteLogDif, fiveMinuteLogDif, hourLogDif, fourHourLogDif
      global twentyMinuteMomentum, fiveMinuteMomentum, hourMomentum, fourHourMomentum
      global twentyMinuteStability, fiveMinuteStability, hourStability, fourHourStability
      global twentyMinuteLogMax, fiveMinuteLogMax, hourLogMax, fourHourLogMax
      
      central = timezone('US/Central')
      now = datetime.now(central)
      analysisTime=now.strftime("%H:%M:%S.%f")
      
      print(len(hourFirst[prID]))
      print(minutes)

      if(len(minuteDeltas[prID]) >= 5):
            # print("\nPerforming Data Analysis: \n")
            # print('Minute Log Dif: \n')
            # print(prID)
            i = -1
            deltaCur = float(minuteDeltas[prID][-1])
            
            I = 1.0      
            if(deltaCur < 0):
                I = -1.0
                
            avgDelt = 0.00
            maxDelt = 0.00
            
            momentum = 0.00
            momentumAvg = 0.00
            pos = 0
            neg = 0
            
            avgPrice = 0.00
            oscillations = 0
            
            p1 = 0
            tmpMax = 0.00
            tmpMin = 0.00
            posMaxSum = 0.00
            negMinSum = 0.00
            prevMax = 0.00
            prevMin = 0.00
            
            momI = 1
            
            j = -1
            k = -1
            
            
            while(i >= -5):
                tmpCur = float(minuteDeltas[prID][i])
                tmpCurA = math.fabs(tmpCur)
                momentumAvg = momentumAvg + tmpCur
                if(tmpCurA > maxDelt):
                    maxDelt = tmpCurA
                if(tmpCur > 0):
                    pos = pos + 1
                if(tmpCur < 0):
                    neg = neg + 1
                avgDelt = avgDelt + tmpCurA
                i = i - 1
                
                
            momentumAvg = momentumAvg/5
            
           
            
                
                
            while(j >= -5):
                p = minuteFirst[prID][j]
                avgPrice = avgPrice + p
                j = j -1
                
                
            avgPrice = (avgPrice/5) + .00000001
            p1 = avgPrice
            
            while(k >= -5):
                p2 = minuteFirst[prID][k]
                # print('avgprice: ' + str(avgPrice))
                # print('prev price: '+ str(p1))
                # print('current price: ' + str(p2))
                # print('tmp Max: ' + str(tmpMax))
                # print('tmp Min: ' + str(tmpMin))
                # print('oscillations:' + str(oscillations))
                # print('\n')
                
                if(p2 > avgPrice and p1 == avgPrice):
                    oscillations = oscillations + 1
                    tmpMax = p2
                    posMaxSum = posMaxSum + (tmpMax/avgPrice)
                    prevMax = p2
                if(p2 > p1 and p1 > avgPrice):
                    tmpMax = p2
                    posMaxSum = posMaxSum + (tmpMax/avgPrice) - (prevMax/avgPrice)
                    prevMax = p2
                if(p1 > avgPrice and p2 < avgPrice):
                    oscillations = oscillations + 1
                    tmpMin = p2
                    negMinSum = negMinSum + tmpMin/avgPrice
                    prevMin = p2
                if(p2 < avgPrice and p1 == avgPrice):
                    oscillations = oscillations + 1
                    tmpMin = p2
                    negMinSum = negMinSum + tmpMin/avgPrice
                    prevMin = p2
                if(p1 < avgPrice and p2 < p1):
                    tmpMin = p2
                    negMinSum = negMinSum + (tmpMin/avgPrice) - (-1*(prevMin/avgPrice))
                if(p1 < avgPrice and p2 > avgPrice):
                    oscillations = oscillations + 1
                    tmpMax = p2
                    posMaxSum = posMaxSum + tmpMax/avgPrice
                    prevMax = p2
                k = k - 1
                p1 = p2
            
            
            stabilitymin = min(math.fabs(negMinSum), math.fabs(posMaxSum))
            osc2 = math.log(oscillations + 1)
            stability = stabilitymin*osc2
               
            
            # print('stability: ')
            # print(oscillations)
            # print(stability)
            # print('\n')
                
            avgDelt = math.fabs(avgDelt/5)
            deltaCur = math.fabs(deltaCur)
            # print('deltas: ')
            # print(avgDelt)
            # print('\n')
           
            
            Tr = 2/avgDelt
            deltaCurT = deltaCur*Tr
            LogDif = math.log1p(deltaCurT)/math.log1p(2)
            LogDifMax = math.log1p(deltaCur)/math.log1p(maxDelt)
            LogDifMax = LogDifMax*I
            LogDif = LogDif*I
            # print('LogDif: ')
            # print(LogDif)
            # print('\n')
          
        
            fiveMinuteLogDif[prID]['value'].append(LogDif)
            fiveMinuteLogMax[prID]['value'].append(LogDifMax)
            fiveMinuteMomentum[prID]['value'].append(momentumAvg)
            fiveMinuteStability[prID]['value'].append(stability)
            fiveMinuteLogDif[prID]['time'].append(analysisTime)
            fiveMinuteLogMax[prID]['time'].append(analysisTime)
            fiveMinuteMomentum[prID]['time'].append(analysisTime)
            fiveMinuteStability[prID]['time'].append(analysisTime)
            
            # print('5 minute momentum: ' + str(momentum))
            
           
            
            
      if(len(fiveMinuteDeltas[prID]) >= 4 and minutes%5 == 0):  
            # print('\nFive Minute Log Dif:\n')
            # print(fiveMinuteDeltas[prID])
            i = -1
            deltaCur = float(fiveMinuteDeltas[prID][-1])
            I = 1.0
            if(deltaCur < 0):
                I = -1.0
            
            avgDelt = 0.00
            maxDelt = 0.00
              
            momentum = 0.00
            momentumAvg = 0.00
            pos = 0
            neg = 0
            
            stability = 0.0        
            
            
            avgPrice = 0.00
            oscillations = 0
            
            p1 = 0
            tmpMax = 0.00
            tmpMin = 0.00
            posMaxSum = 0.00
            negMinSum = 0.00
            
            momI = 1
            
            j = -1
            k = -1
            
            while(i >= -4):
                tmpCur = float(fiveMinuteDeltas[prID][i])
                tmpCurA = math.fabs(tmpCur)
                momentumAvg = momentumAvg + tmpCur
                if(tmpCurA > maxDelt):
                    maxDelt = tmpCurA            
                if(tmpCur > 0):
                    pos = pos + 1
                if(tmpCur < 0):
                    neg = neg + 1
                avgDelt = avgDelt + tmpCurA
                i = i - 1
                
            while(j >= -4):
                p = fiveMinuteFirst[prID][j]
                avgPrice = avgPrice + p
                j = j -1
                
                
            avgPrice = (avgPrice/4) + .00000001
            p1 = avgPrice
            
            while(k >= -4):
                p2 = fiveMinuteFirst[prID][k]
                # print('avgprice: ' + str(avgPrice))
                # print('prev price: '+ str(p1))
                # print('current price: ' + str(p2))
                # print('tmp Max: ' + str(tmpMax))
                # print('tmp Min: ' + str(tmpMin))
                # print('oscillations:' + str(oscillations))
                # print('\n')
                
                if(p2 > avgPrice and p1 == avgPrice):
                    oscillations = oscillations + 1
                    tmpMax = p2
                    posMaxSum = posMaxSum + (tmpMax/avgPrice)
                    prevMax = p2
                if(p2 > p1 and p1 > avgPrice):
                    tmpMax = p2
                    posMaxSum = posMaxSum + (tmpMax/avgPrice) - (prevMax/avgPrice)
                    prevMax = p2
                if(p1 > avgPrice and p2 < avgPrice):
                    oscillations = oscillations + 1
                    tmpMin = p2
                    negMinSum = negMinSum + tmpMin/avgPrice
                    prevMin = p2
                if(p2 < avgPrice and p1 == avgPrice):
                    oscillations = oscillations + 1
                    tmpMin = p2
                    negMinSum = negMinSum + tmpMin/avgPrice
                    prevMin = p2
                if(p1 < avgPrice and p2 < p1):
                    tmpMin = p2
                    negMinSum = negMinSum + (tmpMin/avgPrice) - (-1*(prevMin/avgPrice))
                if(p1 < avgPrice and p2 > avgPrice):
                    oscillations = oscillations + 1
                    tmpMax = p2
                    posMaxSum = posMaxSum + tmpMax/avgPrice
                    prevMax = p2
                k = k - 1
                p1 = p2
            
            stabilitymin = min(math.fabs(negMinSum), math.fabs(posMaxSum))
            osc2 = math.log(oscillations + 1)
            stability = stabilitymin*osc2
            
            momentumAvg = momentumAvg/4
               
            
           
            
            
            # print('stability: ')
            # print(oscillations)
            # print(stability)
            # print('\n')
    
                
            avgDelt = math.fabs(avgDelt/5)
            deltaCur = math.fabs(deltaCur)
            
           

            # print('deltas: ')
            # print(avgDelt)
            # print('\n')
            
            
            Tr = 2/avgDelt
            deltaCurT = deltaCur*Tr
            LogDif = math.log1p(deltaCurT)/math.log1p(2)
            LogDifMax = math.log1p(deltaCur)/math.log1p(maxDelt)
            LogDifMax = LogDifMax*I
            # print('LogDif: ')
            LogDif = LogDif*I
            # print(LogDif)
            # print('\n')
            
            
            twentyMinuteLogDif[prID]['value'].append(LogDif)
            twentyMinuteLogMax[prID]['value'].append(LogDifMax)
            twentyMinuteMomentum[prID]['value'].append(momentumAvg)
            twentyMinuteStability[prID]['value'].append(stability)
            twentyMinuteLogDif[prID]['time'].append(analysisTime)
            twentyMinuteLogMax[prID]['time'].append(analysisTime)
            twentyMinuteMomentum[prID]['time'].append(analysisTime)
            twentyMinuteStability[prID]['time'].append(analysisTime)
            # print('20 minute momentum: ' + str(momentum))
          
            
      if(len(fifteenMinuteDeltas[prID]) >= 4 and minutes%15 == 0):
             
            # print('\nFifteen Minute Log Dif: \n') 
            i = -1
            deltaCur = float(fifteenMinuteDeltas[prID][-1])
          
            
            I = 1.0      
            if(deltaCur < 0):
                I = -1.0
                
            
                
                
            avgDelt = 0.00
            maxDelt = 0.00
              
            momentum = 0.00
            momentumAvg = 0.00
            pos = 0
            neg = 0
            
            stability = 0.0        
            
            
            avgPrice = 0.00
            oscillations = 0
            
            p1 = 0
            tmpMax = 0.00
            tmpMin = 0.00
            posMaxSum = 0.00
            negMinSum = 0.00
            
            momI = 1
            
            j = -1
            k = -1
            
            while(i >= -4):
                tmpCur = float(fifteenMinuteDeltas[prID][i])
                tmpCurA = math.fabs(tmpCur)
                momentumAvg = momentumAvg + tmpCur
                if(tmpCurA > maxDelt):
                    maxDelt = tmpCurA
                if(tmpCur > 0):
                    pos = pos + 1
                if(tmpCur < 0):
                    neg = neg + 1
                avgDelt = avgDelt + tmpCurA
                i = i - 1
                
            while(j >= -4):
                p = fifteenMinuteFirst[prID][j]
                avgPrice = avgPrice + p
                j = j -1
                
                
            avgPrice = (avgPrice/4) + .00000001
            p1 = avgPrice
                
                
            while(k >= -4):
                p2 = fifteenMinuteFirst[prID][k]
                # print('avgprice: ' + str(avgPrice))
                # print('prev price: '+ str(p1))
                # print('current price: ' + str(p2))
                # print('tmp Max: ' + str(tmpMax))
                # print('tmp Min: ' + str(tmpMin))
                # print('oscillations:' + str(oscillations))
                # print('\n')
                
                if(p2 > avgPrice and p1 == avgPrice):
                    oscillations = oscillations + 1
                    tmpMax = p2
                    posMaxSum = posMaxSum + (tmpMax/avgPrice)
                    prevMax = p2
                if(p2 > p1 and p1 > avgPrice):
                    tmpMax = p2
                    posMaxSum = posMaxSum + (tmpMax/avgPrice) - (prevMax/avgPrice)
                    prevMax = p2
                if(p1 > avgPrice and p2 < avgPrice):
                    oscillations = oscillations + 1
                    tmpMin = p2
                    negMinSum = negMinSum + tmpMin/avgPrice
                    prevMin = p2
                if(p2 < avgPrice and p1 == avgPrice):
                    oscillations = oscillations + 1
                    tmpMin = p2
                    negMinSum = negMinSum + tmpMin/avgPrice
                    prevMin = p2
                if(p1 < avgPrice and p2 < p1):
                    tmpMin = p2
                    negMinSum = negMinSum + (tmpMin/avgPrice) - (-1*(prevMin/avgPrice))
                if(p1 < avgPrice and p2 > avgPrice):
                    oscillations = oscillations + 1
                    tmpMax = p2
                    posMaxSum = posMaxSum + tmpMax/avgPrice
                    prevMax = p2
                k = k - 1
                p1 = p2
            
            
            stabilitymin = min(math.fabs(negMinSum), math.fabs(posMaxSum))
            osc2 = math.log(oscillations + 1)
            stability = stabilitymin*osc2
  
               
            momentumAvg = momentumAvg/4
                
            
            
            # print('stability: ')
            # print(oscillations)
            # print(stability)
            # print('\n')
    
                
            avgDelt = math.fabs(avgDelt/4)
            deltaCur = math.fabs(deltaCur)


            # print('deltas: ')
            # print(deltaCur)
            # print('max' + str(maxDelt))
            # print('avg' + str(avgDelt))
            # print('\n')
            
            
            Tr = 2/avgDelt
            deltaCurT = deltaCur*Tr
            LogDif = math.log1p(deltaCurT)/math.log1p(2)
            LogDifMax = math.log1p(deltaCur)/math.log1p(maxDelt)
            LogDifMax = LogDifMax*I
            # print('LogDif: ')
            LogDif = LogDif*I
            # print(LogDif)
            # print('\n')
            
            hourLogDif[prID]['value'].append(LogDif)
            hourLogMax[prID]['value'].append(LogDifMax)
            hourMomentum[prID]['value'].append(momentumAvg)
            hourStability[prID]['value'].append(stability)
            hourLogDif[prID]['time'].append(analysisTime)
            hourLogMax[prID]['time'].append(analysisTime)
            hourMomentum[prID]['time'].append(analysisTime)
            hourStability[prID]['time'].append(analysisTime)
            # print('One hour momentum: ' + str(momentum))
          
          

                 
                 
      if(len(hourFirst[prID]) >= 5 and minutes == 0):
             
            # print('\nHour Log Dif: \n') 
            i = -1
            A = float(hourFirst[prID][i])
            B = float(hourFirst[prID][i-1])
            C = (A - B)/B
            deltaCur = C
            
            
            I = 1.0      
            if(deltaCur < 0):
                I = -1.0
                
            
                
                
            avgDelt = 0.00
            maxDelt = 0.00
              
            momentum = 0.00
            momentumAvg = 0.00
            pos = 0
            neg = 0
            
            stability = 0.0        
            
            
            avgPrice = 0.00
            oscillations = 0
            
            p1 = 0
            tmpMax = 0.00
            tmpMin = 0.00
            posMaxSum = 0.00
            negMinSum = 0.00
            
            momI = 1
            
            j = -1
            k = -1
            
            while(i >= -4):
                tmpA = float(hourFirst[prID][i])
                tmpB = float(hourFirst[prID][i-1])
                tmpCur = (tmpA - tmpB)/tmpB
                momentumAvg = momentumAvg + tmpCur
                if(tmpCurA > maxDelt):
                    maxDelt = tmpCurA
                if(tmpCur > 0):
                    pos = pos + 1
                if(tmpCur < 0):
                    neg = neg + 1
                i = i - 1
                
            while(j >= -4):
                p = hourFirst[prID][j]
                avgPrice = avgPrice + p
                j = j -1
                
                
            avgPrice = (avgPrice/4) + .00000001
            p1 = avgPrice
                
                
            while(k >= -4):
                p2 = hourFirst[prID][k]
                # print('avgprice: ' + str(avgPrice))
                # print('prev price: '+ str(p1))
                # print('current price: ' + str(p2))
                # print('tmp Max: ' + str(tmpMax))
                # print('tmp Min: ' + str(tmpMin))
                # print('oscillations:' + str(oscillations))
                # print('\n')
                
                if(p2 > avgPrice and p1 == avgPrice):
                    oscillations = oscillations + 1
                    tmpMax = p2
                    posMaxSum = posMaxSum + (tmpMax/avgPrice)
                    prevMax = p2
                if(p2 > p1 and p1 > avgPrice):
                    tmpMax = p2
                    posMaxSum = posMaxSum + (tmpMax/avgPrice) - (prevMax/avgPrice)
                    prevMax = p2
                if(p1 > avgPrice and p2 < avgPrice):
                    oscillations = oscillations + 1
                    tmpMin = p2
                    negMinSum = negMinSum + tmpMin/avgPrice
                    prevMin = p2
                if(p2 < avgPrice and p1 == avgPrice):
                    oscillations = oscillations + 1
                    tmpMin = p2
                    negMinSum = negMinSum + tmpMin/avgPrice
                    prevMin = p2
                if(p1 < avgPrice and p2 < p1):
                    tmpMin = p2
                    negMinSum = negMinSum + (tmpMin/avgPrice) - (-1*(prevMin/avgPrice))
                if(p1 < avgPrice and p2 > avgPrice):
                    oscillations = oscillations + 1
                    tmpMax = p2
                    posMaxSum = posMaxSum + tmpMax/avgPrice
                    prevMax = p2
                k = k - 1
                p1 = p2
            
            
            stabilitymin = min(math.fabs(negMinSum), math.fabs(posMaxSum))
            osc2 = math.log(oscillations + 1)
            stability = stabilitymin*osc2
               
                
            momentumAvg = momentumAvg/4
            
          
         
            
            # print('stability: ')
            # print(oscillations)
            # print(stability)
            # print('\n')
    
                
            avgDelt = math.fabs(avgDelt/4)
            deltaCur = math.fabs(deltaCur)


            # print('deltas: ')
            # print(avgDelt)
               
            
            
            # print('\n')
            
            
            Tr = 2/avgDelt
            deltaCurT = deltaCur*Tr
            LogDif = math.log1p(deltaCurT)/math.log1p(2)
            LogDifMax = math.log1p(deltaCur)/math.log1p(maxDelt)
            LogDifMax = LogDifMax*I
            # print('LogDif: ')
            LogDif = LogDif*I
            # print(LogDif)
            # print('\n')
            fourHourLogDif[prID].append(LogDif)
            fourHourLogMax[prID].append(LogDifMax)
            fourHourMomentum[prID].append(momentumAvg)
            fourHourStability[prID].append(stability)
            # print('Four hour momentum: ' + str(momentum))
            
            
      if(len(hourFirst[prID]) >= 7 and minutes == 0):
          
            # print('\nSix Hour Momentum: \n') 
            i = -1
                
            momI = 1
        
            momentum = 0.00
            momentumAvg = 0.00
            
            neg = 0
            pos = 0
          
          
            while(i >= -6):
                
                tmpA = float(hourFirst[prID][i])
                tmpB = float(hourFirst[prID][i-1])
                tmpCur = (tmpA - tmpB)/tmpB
                momentumAvg = momentumAvg + tmpCur
                if(tmpCur > 0):
                    pos = pos + 1
                if(tmpCur < 0):
                    neg = neg + 1
                i = i - 1
               
                
            momentumAvg = momentumAvg/6
           
         
             
            sixHourMomentum[prID].append(momentumAvg)
            
            
      if(len(hourFirst[prID]) >= 13 and minutes == 0):
          
            # print('\nTwelve Hour Momentum: \n') 
            i = -1
                
            momI = 1
        
            momentum = 0.00
            momentumAvg = 0.00
          
            pos = 0
            neg = 0
            
            
            while(i >= -12):
                tmpA = float(hourFirst[prID][i])
                tmpB = float(hourFirst[prID][i-1])
                tmpCur = (tmpA - tmpB)/tmpB
                momentumAvg = momentumAvg + tmpCur
                if(tmpCur > 0):
                    pos = pos + 1
                if(tmpCur < 0):
                    neg = neg + 1
                i = i - 1
               
            momentumAvg = momentumAvg/12

             
             
            
            twelveHourMomentum[prID].append(momentumAvg)
            
      if(len(hourFirst[prID]) >= 73 and minutes == 0):
          
            i = -1
                
            momI = 1
        
            momentum = 0.00
            momentumAvg = 0.00
          
            pos = 0
            neg = 0
            
            
            while(i >= -72):
                tmpA = float(hourFirst[prID][i])
                tmpB = float(hourFirst[prID][i-1])
                tmpCur = (tmpA - tmpB)/tmpB
                momentumAvg = momentumAvg + tmpCur
                if(tmpCur > 0):
                    pos = pos + 1
                if(tmpCur < 0):
                    neg = neg + 1
                i = i - 1
               
            momentumAvg = momentumAvg/72

           
          
             
             
         
            threeDayMomentum[prID].append(momentumAvg)

            # Three Day Momentum
          
      if(len(hourFirst[prID]) >= 169 and minutes == 0):
          
            i = -1
                
            momI = 1
        
            momentum = 0.00
            momentumAvg = 0.00
          
            pos = 0
            neg = 0
            
            
            while(i >= -168):
                tmpA = float(hourFirst[prID][i])
                tmpB = float(hourFirst[prID][i-1])
                tmpCur = (tmpA - tmpB)/tmpB
                momentumAvg = momentumAvg + tmpCur
                if(tmpCur > 0):
                    pos = pos + 1
                if(tmpCur < 0):
                    neg = neg + 1
                i = i - 1
               
            momentumAvg = momentumAvg/168

            
             
             
            
            sevenDayMomentum[prID].append(momentumAvg)
            # 7 Day Momentum
            
      if(len(hourFirst[prID]) >= 721 and minutes == 0):
          
            i = -1
                
            momI = 1
        
            momentum = 0.00
            momentumAvg = 0.00
          
            pos = 0
            neg = 0
            
            
            while(i >= -720):
                tmpA = float(hourFirst[prID][i])
                tmpB = float(hourFirst[prID][i-1])
                tmpCur = (tmpA - tmpB)/tmpB
                momentumAvg = momentumAvg + tmpCur
                if(tmpCur > 0):
                    pos = pos + 1
                if(tmpCur < 0):
                    neg = neg + 1
                i = i - 1
               
            momentumAvg = momentumAvg/720


             
           
            oneMonthMomentum[prID].append(momentumAvg)

            # 30 Day Momentum
                 
           



def ScheduleChecks():
    global sec1float, min1int, hour1int, secfloat
    global job1, scheduler
    scheduler = BackgroundScheduler()
   
    
    print(hours)
     
    job1 = scheduler.add_job(checkTicker, 'interval', id='priceCheck',seconds =1, max_instances= 1)
     

    central = timezone('US/Central')
    now = datetime.now(central)
    startTime=now.strftime("%H:%M:%S.%f")
    sec1 = now.strftime('%S.%f')
    min1 = now.strftime('%M')
    hour1 = now.strftime('%H')
    
    print(min1)
    print(sec1)
    sec1float = float(sec1) + 1
    min1int = int(min1)
    hour1int = int(hour1)

    if(intervalType == 'S'):  
        scheduler.start()
        time.sleep(intervalLength)
        job1.remove()
        scheduler.shutdown()
        

    if(intervalType == 'M'):
        scheduler.start()
        time.sleep(int(intervalLength*60))
        job1.remove()
        
    if(intervalType == 'H'):
        scheduler.start()
        sleepvar = (intervalLength*60*60)
        sleepvar = sleepvar + (minLength*60)
        time.sleep(int(sleepvar))
        job1.remove()
        scheduler.shutdown()
       
        
def updateBalance():
    accounts = auth_client.get_accounts()
    
    for acc in accounts:
        cur = acc['currency']
        id = acc['id']
        balance = acc['balance']
        accountList[cur] = id
        balanceList[cur] = balance
    
        
def getAccounts():
    global accountList, balanceList

    updateBalance()
        
    setUp()
    
    
def editBuySell():
    

     for cur in currencyIL:
    
         buyLen = len(BuySellCopy[cur]['BuyTime'])
         sellLen = len(BuySellCopy[cur]['SellTime'])
         
         if(buyLen > sellLen):
             BuySellCopy[cur]['SellTime'].append('NA')
             BuySellCopy[cur]['SellPrice'].append(0.00)
             BuySellCopy[cur]['ProfitPercentage'].append(0.00)
             BuySellCopy[cur]['TotalMinutes'].append('NA')
             

        
def createDataFrames():
    global BuySellCopy
    
    BuySellCopy = copy.deepcopy(BuySellList)
    editBuySell()
    central = timezone('US/Central')
    now = datetime.now(central)
    
    for cur in currencyIL:


        endTime=now.strftime("%D.%H.%M.")
        endTime = endTime.replace('/', '.')
        
        curID = cur.split('-')[0]
        folderpath = "enter folder path to save data"
        folderPath2 = folderpath + endTime
        filepath = folderPath2 + '/' + curID + '.' + endTime
        BuySellName = filepath + 'BuySell' + '.csv'
        hourlyFirstName = filepath + 'HourlyFirst' + '.csv'
        fifteenMinuteName = filepath + 'fifteenMinuteFirst' + '.csv'
        fiveMinuteName = filepath + 'fiveMinuteFirst' + '.csv'
        minuteName = filepath + 'MinuteFirst' + '.csv'
        
        if not os.path.exists(folderPath2):
            os.makedirs(folderPath2)
            
    
        hourlyData = pd.DataFrame(hourFirst[cur])
        hourlyData.to_csv(hourlyFirstName, sep='\t')
      
        fifteenMinuteData = pd.DataFrame(fifteenMinuteFirst[cur])
        fifteenMinuteData.to_csv(fifteenMinuteName, sep = '\t')
        fiveMinuteData = pd.DataFrame(fiveMinuteFirst[cur])
        fiveMinuteData.to_csv(fiveMinuteName, sep='\t')
        minuteData = pd.DataFrame(minuteFirst[cur])
        minuteData.to_csv(minuteName, sep='\t')
        

        
if(setUpInput != 'y'):     
    t = threading.Thread(target=getAccounts)
    t.start()
    t.join()
    
elif(setUpInput == 'y'):
    setUpBool = True
    t = threading.Thread(target=setUpWithPrevData)
    t.start()
    t.join()
    updateBalance()

            
print('Would you like to add previous Buy Information? Enter y to input information')
buyBoolean = input()

if(buyBoolean == 'y'):
    curID = 'y'
    while(curID != ''):
        print('Enter the Currency ID: ' '\nPress Enter to Exit')
        curID = input()
        if(curID == ''):
            break
        print('Enter the Buy Time: ')
        buyTime = input()
        BuySellList[curID]['BuyTime'].append(buyTime)
        print('Enter the Buy Price: ')
        buyPrice = input()
        BuySellList[curID]['BuyPrice'].append(buyPrice)

    
t1 = threading.Thread(target=ScheduleChecks)   
t1.start()
t1.join()

# ScheduleChecks()
final = threading.Thread(target=createDataFrames())  
final.start()


print("Press Q then Enter to stop Thread...")       
stopString = input()
if(stopString == 'Q'):
    job1.remove()
    scheduler.shutdown()
    # t1.join()




















        
    
