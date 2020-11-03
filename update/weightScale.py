#!/usr/bin/env python3
import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
import numpy,os,json
import gSheet

rootPath = os.path.dirname(os.path.abspath(__file__))
dataPath = rootPath+'/data'
configPath = dataPath + '/brsHiveInfo.json'
configJson = json.load(open(configPath))

def getRawData(rawDataCount = 3):
    GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
    hx = HX711(dout_pin=5,
               pd_sck_pin=6,
               channel='A',
               gain=128)
    hx.reset()
    data = hx.get_raw_data(rawDataCount)  # get raw data reading from hx711
    GPIO.cleanup()
    return data


def getBoxPlotList (dataList):
    #arr = [12287.0, 12287.0, 2047.0, 16383.0, 24574.5, 16383.0, 8191.0, 4095.0, 16383.0, 16383.0]
    xmin = (min(dataList))
    xmax = (max(dataList))
    xmedian = (numpy.median(dataList))
    xq1 = numpy.percentile(dataList, 25)
    xq3 = numpy.percentile(dataList, 75)
    iqr = xq3 - xq1
    uprBound = xq3 + 1.5 * iqr
    lwrBound = xq1 - 1.5 * iqr
    newArr = []
    outlier = []
    for i in dataList:
        if i > uprBound:
            i = uprBound
            outlier.append(i)
        elif i < lwrBound:
            i = lwrBound
            outlier.append(i)
        newArr.append(i)
    print('Box plot found outlier count : {}'.format(len(outlier)))
    return newArr
    #print(xmedian)
    #print(xq1)
    #print(xq3)
    #print(uprBound)
    #print(lwrBound)
    #print('min {}'.format(min(dataList)))
    #print('max {}'.format(max(dataList)))
    #print('mean {}'.format(sum(dataList) / len(dataList)))
    #print('median {}'.format(numpy.median(dataList)))

def getRefineRawData(count=10):
    rawDataList = []
    for i in range(count):
        raw = getRawData()
        rawMean = numpy.mean(raw)
        rawDataList.append(rawMean)
        print ('count {}/{} Calculating Raw {}'.format(i,count,rawMean))
    data = getBoxPlotList(rawDataList)
    return data

def captureZero(*_):
    input('Enter to set zero :')
    rawData = getRefineRawData()
    measures = numpy.mean(rawData)
    configJson['config']['weightAdjZero'] = measures
    json.dump(configJson, open(configPath, 'w'), indent=4)
    gSheet.updateConfigValue(configJson['idName'],'config_weightAdjZero',measures)
    print('Set zero measures finish')

def captureDivider(*_):
    inputTarget = input('Insert Something and Enter Weight Target (gram) :')
    rawData = getRefineRawData()
    measures = numpy.mean(rawData)
    zeroAdj = configJson['config']['weightAdjZero']
    measuresAdj = measures - zeroAdj
    divider = 1.0
    gram = measuresAdj / divider
    for i in range(100):
        divider += 0.01
        gram = measuresAdj / divider
        print(gram)
        if round(gram, 0) <= int(inputTarget):
            print('Divider is {}'.format(divider))
            configJson['config']['weightDivider'] = divider
            json.dump(configJson, open(configPath, 'w'), indent=4)
            gSheet.updateConfigValue(configJson['idName'], 'config_weightDivider', divider)
            break

def getWeightGram(*_):
    rawData = getRefineRawData()
    measures = numpy.mean(rawData)
    zeroAdj = configJson['config']['weightAdjZero']
    divider = configJson['config']['weightDivider']
    measuresAdj = measures-zeroAdj
    gram = measuresAdj /divider
    return gram

def getWeightKg(*_):
    gram = getWeightGram()
    kilogram = gram/1000
    return kilogram

if __name__=='__main__':
    captureZero()
    captureDivider()
    print('Finished Calibrate')
