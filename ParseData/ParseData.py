#coding=utf-8
import pandas as pd
import numpy as np

ItemDic ={"SerialNumber":"SN","Test Pass/Fail Status":"Result","StartTime":"Time","BestPWM":"PWM","Centerx":"Centerx","Centery":"Centery","DarkNoise":"DarkNoise","GlobalFactora":"GlobalFactora","GlobalFactorb":"GlobalFactorb","GlobalFactorc":"GlobalFactorc","GridBlockMax":"GridBlockMax","GridBlockMin":"GridBlockMin","ImageQuality":"ImageQuality","maxPWMBrightness":"maxPWMBrightness","PWM20Brightness":"Brightness","PWM20BrightnessRaw":"PWM20BrightnessRaw","RetryCounter":"RetryCounter","Uniformity":"Uniformity"}


OriginalData = pd.read_csv("Data.csv",header = None)
NewData = pd.read_csv("DataHearder.csv",header = None)
myData = pd.DataFrame()
for i in range(0,NewData.shape[1]):
    NewCurrentItem = NewData[i][0]
    if NewCurrentItem in ItemDic:
        for j in range(0,OriginalData.shape[1]):
            OriginalCurrentItem = OriginalData[j][0]
            if OriginalCurrentItem == ItemDic[NewCurrentItem]:
                myData.loc[:,NewCurrentItem] = OriginalData[j][3:]
    else:
        myData.loc[:,NewCurrentItem] = OriginalData[0][3:]
        myData.loc[:,NewCurrentItem] = ""
myData.to_csv("NewData.csv",index=False)

DataHeard = pd.read_csv("DataHearder.csv")
Data = pd.read_csv("NewData.csv")
a = DataHeard.append(Data)
a.to_csv("NewData.csv",index=False)



