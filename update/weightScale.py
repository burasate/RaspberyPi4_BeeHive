#!/usr/bin/env python3
import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
import numpy,os,json,time
import gSheet

rootPath = os.path.dirname(os.path.abspath(__file__))
dataPath = rootPath+'/data'
configPath = dataPath + '/brsHiveInfo.json'
configJson = json.load(open(configPath))

weightRawDataSample = configJson['config']['weightRawDataSample']
print ('Set Weight Raw Data Sample : {}'.format(weightRawDataSample))

measuresErrorLimit = 5.0

def getRawData(rawDataCount = weightRawDataSample):
    GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
    hx = HX711(dout_pin=5,
               pd_sck_pin=6,
               channel = 'A',
               gain = 128)
    hx.reset()
    data = hx.get_raw_data(rawDataCount)  # get raw data reading from hx711
    print ('hx711 raw : {}'.format(data))
    GPIO.cleanup()
    return data


def getBoxPlotList (dataList):
    xq1 = numpy.percentile(dataList, 25)
    xq3 = numpy.percentile(dataList, 75)
    iqr = xq3 - xq1
    uprBound = xq3 + 1.5 * iqr
    lwrBound = xq1 - 1.5 * iqr
    newArr = []
    outlier = []
    for i in dataList:
        if i < 0 or i > uprBound or i < lwrBound:
            outlier.append(i)
        else:
            newArr.append(i)
    print('Box plot found outlier count : {}'.format(len(outlier)))
    return newArr

def captureZero(*_):
    input('Enter to set zero :')
    while True:
        raw = getRawData()
        boxPlot = getBoxPlotList(raw)
        measures = numpy.mean(boxPlot)
        measuresMedian = numpy.median(boxPlot)
        measuresError = abs(measures - measuresMedian)
        print('mean : {}  median : {} , error : {}'.format(measures, measuresMedian, measuresError))
        if measuresError < measuresErrorLimit:
            configJson['config']['weightAdjZero'] = measures
            json.dump(configJson, open(configPath, 'w'), indent=4)
            gSheet.updateConfigValue(configJson['idName'], 'config_weightAdjZero', measures)
            print('Set zero measures finish : raw {}'.format(measures))
            break

def captureDivider(*_):
    inputTarget = input('Insert Something and Enter Weight Target (gram) :')
    while True:
        raw = getRawData()
        boxPlot = getBoxPlotList(raw)
        measures = numpy.mean(boxPlot)
        measuresMedian = numpy.median(boxPlot)
        measuresError = abs(measures - measuresMedian)
        print('mean : {}  median : {} , error : {}'.format(measures, measuresMedian, measuresError))
        if measuresError < measuresErrorLimit:
            break
    zeroAdj = configJson['config']['weightAdjZero']
    measuresAdj = measures - zeroAdj
    divider = 1.0
    gram = measuresAdj / divider
    #for i in range(100):
    while True:
        divider += 0.1
        gram = measuresAdj / divider
        print('Calculating... {} g'.format(gram))
        if round(gram, 0) <= int(inputTarget):
            print('Divider is {}'.format(divider))
            configJson['config']['weightDivider'] = divider
            json.dump(configJson, open(configPath, 'w'), indent=4)
            gSheet.updateConfigValue(configJson['idName'], 'config_weightDivider', divider)
            break

def getWeightGram(*_):
    while True:
        raw = getRawData()
        boxPlot = getBoxPlotList(raw)
        measures = numpy.mean(boxPlot)
        measuresMedian = numpy.median(boxPlot)
        measuresError = abs(measures - measuresMedian)
        print('mean : {}  median : {} , error : {}'.format(measures, measuresMedian, measuresError))
        if measuresError < measuresErrorLimit:
            break
    zeroAdj = configJson['config']['weightAdjZero']
    divider = configJson['config']['weightDivider']
    #rel_weight / (rel_reading - init_reading)
    measuresAdj = measures-zeroAdj
    gram = measuresAdj /divider
    return gram

def getWeightKg(*_):
    gram = getWeightGram()
    kilogram = gram/1000
    return kilogram

if __name__=='__main__':
    inputPrompt = input('HX711 Callibrate ?  y/n :')
    if inputPrompt.lower() == 'y':
        captureZero()
        captureDivider()
        print('Finished Calibrate')
    inputPrompt = input('y = Test Weight (Kg) | n = Testing Raw Data  y/n :')
    if inputPrompt.lower() == 'y':
        #Test After Callibrate
        while True:
            weightTest = getWeightKg()
            print('now weight is : {}'.format(weightTest))
    else:
        #Test Input
        while True :
            raw = getRawData()
            boxPlot = getBoxPlotList(raw)
            measures = numpy.mean(boxPlot)
            measuresMedian = numpy.median(boxPlot)
            measuresError = abs(measures - measuresMedian)
            print('mean : {}  median : {} , error : {}'.format(measures, measuresMedian, measuresError))
