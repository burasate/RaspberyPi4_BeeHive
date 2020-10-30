#!/usr/bin/python
import sys
import Adafruit_DHT

sensor = Adafruit_DHT.DHT22
pin = 8

def getRawData(*_):
    #print(Adafruit_DHT.read_retry(sensor, pin))
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        print ('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        data = {'temperature':temperature,'humidity':humidity}
        return data
    else:
        print ('DHT22 Failed to get reading. Try again!')

def getTemperature(*_):
    data = getRawData()
    return data['temperature']

def getHumidity(*_):
    data = getRawData()
    return data['humidity']

if __name__=='__main__':
    print('Temperature {} *c'.format(getTemperature()))
    print('Humidity {} %'.format(getHumidity()))