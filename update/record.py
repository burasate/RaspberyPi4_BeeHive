import os,json
import datetime as dt
import csvFile,gSheet
import random
import weightScale,temperature

rootPath = os.path.dirname(os.path.abspath(__file__))
dataPath = rootPath+'/data'
recordPath = dataPath+'/record'
dumpFile = recordPath+'/tempRecord.csv'
historyFile = recordPath+'/recordHistory.csv'
configPath = dataPath + '/brsHiveInfo.json'
configJson = json.load(open(configPath))

#header = googleSheet.getWorksheetColumnName('Record')
header = ['Date', 'Time', 'Name', 'Weight', 'Temperature', 'Humidity']

def createDumpFile(*_):
    try:
        os.remove(dumpFile)
        file = open(dumpFile, 'w')
    except:
        file = open(dumpFile,'w')
    finally:
        file.close()

def dumpRecordData(*_):
    col = [None] * len(header)
    dataS = {
        'date' : dt.datetime.now().date().isoformat(),
        'time' : dt.datetime.now().time().isoformat(),
        'weight' : weightScale.getWeightKg(),
        'temperature' : temperature.getTemperature(),
        'humidity' : temperature.getTemperature(),
        'name' : configJson['idName']
    }
    for colName in header:
        index = header.index(colName)
        col[index] = dataS[colName.lower()]
    csvFile.addRow(dumpFile, col)
    #print(col)

def writeRecordData(*_):
    try:
        open(historyFile)
    except:
        csvFile.create(historyFile,header)
    finally:
        rowCount = len(csvFile.getAll(dumpFile))
        for i in range(rowCount):
            col = csvFile.getRow(dumpFile, 0)
            csvFile.addRow(historyFile,col)
            try:
                gSheet.addRow('Record', col)
            except:
                pass
            csvFile.deleteRow(dumpFile,0)


if __name__=='__main__':
    createDumpFile()
    for i in range(50):
        dumpRecordData()
    writeRecordData()