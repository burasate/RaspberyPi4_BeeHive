import os,json
import datetime as dt
import csvFile,gSheet,lineNotify
import piStat
import weightScale,temperature

rootPath = os.path.dirname(os.path.abspath(__file__))
dataPath = rootPath+'/data'
recordPath = dataPath+'/record'
dumpFile = recordPath+'/tempRecord.csv'
historyFile = recordPath+'/recordHistory.csv'
configPath = dataPath + '/brsHiveInfo.json'
configJson = json.load(open(configPath))

#Notify
if bool(configJson['config']['lineStartupAlert']):
    lineNotify.sendNotifyMassage('{} is working now'.format(configJson['idName']))

#column header
try:
    header = gSheet.getWorksheetColumnName('Record')
except:
    header = ['Date', 'Time', 'Name', 'Weight', 'Temperature', 'Humidity']

def createDumpFile(*_):
    try:
        #os.remove(dumpFile)
        file = open(dumpFile, 'w')
    except:
        file = open(dumpFile,'w')
    finally:
        file.close()

def dumpRecordData(*_):
    col = [None] * len(header)
    dataS = {
        'epoch' : dt.datetime.now().timestamp(),
        'date_time' : dt.datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),
        'date' : dt.datetime.now().date().isoformat(),
        'time' : dt.datetime.now().time().isoformat(),
        'year' : dt.datetime.now().year,
        'month' : dt.datetime.now().month,
        'day' : dt.datetime.now().day,
        'hour' : dt.datetime.now().hour,
        'minute' : dt.datetime.now().minute,
        'second' : dt.datetime.now().second,
        'weight' : round(weightScale.getWeightKg(),2),
        'temperature' : round(temperature.getTemperature(),2),
        'humidity' : round(temperature.getHumidity(),2),
        'name' : configJson['idName'],
        'core_temp' : piStat.getCPUTemp(),
        'free_space' : piStat.getFreeSpaceStat()
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
            try:
                #csvFile.addRow(historyFile,col)
                gSheet.addRow('Record', col)
                csvFile.deleteRow(dumpFile,0)
            except:
                print ('cannot add row in database')


if __name__=='__main__':
    createDumpFile()
    for i in range(50):
        dumpRecordData()
    writeRecordData()
