import os,json
import requests
import gSheet

rootPath = os.path.dirname(os.path.abspath(__file__))
dataPath = rootPath+'/data'
configPath = dataPath + '/brsHiveInfo.json'
updateFilePath = requests.get('https://raw.githubusercontent.com/burasate/RaspberyPi4_BeeHive/main/update/update.json').text
fileNameSet = json.loads(updateFilePath)
configJson = json.load(open(configPath))

def updateAllFile(*_):
    #Check Auto Update
    autoUpdate = bool(gSheet.getConfigValue(configJson['idName'], 'config_autoUpdate'))
    onceTimeUpdate = bool(gSheet.getConfigValue(configJson['idName'], 'config_onceTimeUpdate'))
    if autoUpdate:
        print ('System Updating....')
        if onceTimeUpdate:
            gSheet.updateConfigValue(configJson['idName'], 'config_autoUpdate', 0)

    for file in fileNameSet:
        print('Updating {} from {}'.format(file,fileNameSet[file]))
        scriptUpdater = fileNameSet[file]
        mainWriter = open(rootPath + os.sep + file, 'w')
        urlReader = requests.get(scriptUpdater).text
        mainWriter.writelines(urlReader)
        mainWriter.close()
    print('System Updated')

def updateConfig(*_):
    configSheet = gSheet.loadConfigData(idName=configJson['idName'])
    #Update local config
    for k in configSheet:
        if k.__contains__('config'):
            #print(k)
            keyName = k.split('_')[-1]
            #print(keyName)
            #print(configSheet[k])
            configJson['config'][keyName] = configSheet[k]
        elif k == 'description':
            configJson[k] = configSheet[k]
        elif k == 'owner':
            configJson[k] = configSheet[k]
    json.dump(configJson,open(configPath,'w'),indent=4)
    print ('config has been updated')

if __name__ == '__main__':
    updateConfig()
    updateAllFile()