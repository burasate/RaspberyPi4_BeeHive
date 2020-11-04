def printHeader (text):
    print('------------------------------------------------------')
    print(text)
    print('------------------------------------------------------')

printHeader('\nBurasate Smart Hive Base System\n')

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

if bool(configJson['config']['active']):
    #Record
    printHeader('Recording')
    recordInterval = configJson['config']['recordInterval']
    print('Record every {} Minute'.format(recordInterval))

    import record
    record.createDumpFile()
    while True:
        record.dumpRecordData()
        record.writeRecordData()
        time.sleep(recordInterval*60)
else:
    printHeader('Recording cancle')
