#!/usr/bin/env python3
import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
import numpy,os,json
import gSheet

rootPath = os.path.dirname(os.path.abspath(__file__))
dataPath = rootPath+'/data'
configPath = dataPath + '/brsHiveInfo.json'
configJson = json.load(open(configPath))

def getRawData(*_):
    GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
    hx = HX711(dout_pin=5,
               pd_sck_pin=6,
               channel='A',
               gain=64)
    hx.reset()
    data = hx.get_raw_data(50)  # get raw data reading from hx711
    GPIO.cleanup()
    return data

def captureZero(*_):
    input('Set Zero Press Any Key..')
    rawData = getRawData()
    measures = numpy.median(rawData)
    configJson['config']['weightAdjZero'] = measures
    json.dump(configJson, open(configPath, 'w'), indent=4)
    gSheet.updateConfigValue(configJson['idName'],'config_weightAdjZero',measures)
    print('Set zero measures finish')

def captureDivider(*_):
    inputTarget = input('Insert Something and Enter Weight Target (gram) :')
    rawData = getRawData()
    measures = numpy.median(rawData)
    zeroAdj = configJson['config']['weightDivider']
    measuresAdj = measures - zeroAdj
    divider = 1
    gram = measuresAdj / divider
    for i in range(100):
        divider += 1
        gram = measuresAdj / divider
        print(gram)
        if round(gram, 0) <= int(inputTarget):
            print('Divider is {}'.format(divider))
            configJson['config']['weightDivider'] = divider
            json.dump(configJson, open(configPath, 'w'), indent=4)
            gSheet.updateConfigValue(configJson['idName'], 'config_weightDivider', divider)
            break

def getWeightGram(*_):
    rawData = getRawData()
    measures = numpy.median(rawData)
    zeroAdj = configJson['config']['weightDivider']
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

"""
#rawData = getRawData()
rawData = [-60909.3333333333,-60909.33333333333,-60909.33333333333]
measures = numpy.median(rawData)
zeroAdj = -60909.33333333333
measuresAdj = measures - zeroAdj
i = 55
gram = measuresAdj / i
print(gram)
kilogram = round(gram / 1000, 4)
print(kilogram)
"""
"""
while True:
    i += 1
    gram = measuresAdj/i
    print (gram)
    if round(gram,0)<=1500:
        print (i)
        break
"""


