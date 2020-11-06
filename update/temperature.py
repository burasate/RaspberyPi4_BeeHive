#!/usr/bin/python
import boxPlot
import Adafruit_DHT

sensor = Adafruit_DHT.DHT22
pin = 8

temperatureErrorLimit = configJson['config']['temperatureErrorLimit']
print ('Set Temperature Error Limit : {}'.format(temperatureErrorLimit))

def getRawData(*_):
    #print(Adafruit_DHT.read_retry(sensor, pin))
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        #print ('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        #data = {'temperature':temperature,'humidity':humidity}
        return data
    else:
        print ('DHT22 Failed to get reading. Try again!')

def getTemperature(*_):
    while True:
        dataList = []
        for i in range (20):
            data = getRawData()
            dataList.append(data['temperature'])
        dataList = boxPlot.getBoxPlotList(dataList)
        meanMedianError = boxPlot.getMeanMedianErrror(dataList)
        if meanMedianError['error'] < temperatureErrorLimit:
            return meanMedianError['temperature']
            break

def getHumidity(*_):
    while True:
        dataList = []
        for i in range (20):
            data = getRawData()
            dataList.append(data['humidity'])
        dataList = boxPlot.getBoxPlotList(dataList)
        meanMedianError = boxPlot.getMeanMedianErrror(dataList)
        if meanMedianError['error'] < temperatureErrorLimit:
            return meanMedianError['temperature']
            break

if __name__=='__main__':
    print('Temperature {} *c'.format(getTemperature()))
    print('Humidity {} %'.format(getHumidity()))