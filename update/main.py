def printHeader (text):
    print('---------------------------')
    print(text)
    print('---------------------------')

#System Update
printHeader('System Update')

import update
update.updateConfig()
update.updateAllFile()

#Init
import os,time,json

rootPath = os.path.dirname(os.path.abspath(__file__))
dataPath = rootPath+'/data'
configPath = dataPath + '/brsHiveInfo.json'
configJson = json.load(open(configPath))

#Record
printHeader('Recording')
recordInterval = configJson['config']['recordInterval']
print('Record every {} Minute'.format(recordInterval))

import record
record.createDumpFile()
while True:
    record.dumpRecordData()
    record.writeRecordData()
    #time.sleep(recordInterval*60)
    time.sleep(15)