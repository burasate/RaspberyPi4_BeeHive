import os,json
import requests
import gSheet

rootPath = os.path.dirname(os.path.abspath(__file__))
dataPath = rootPath+'/data'
configPath = dataPath + '/brsHiveInfo.json'
configJson = json.load(open(configPath))

updateListURL = 'https://raw.githubusercontent.com/burasate/RaspberyPi4_BeeHive/main/update/update.json'
while True:
    connectStatus = requests.get(updateListURL).status_code
    if connectStatus == 200:
        updateFilePath = requests.get(updateListURL).text
        break
fileNameSet = json.loads(updateFilePath)

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
            url = fileNameSet[file]
            while True:
                connectStatus = requests.get(url).status_code
                print('connecting...')
                if connectStatus == 200:
                    mainWriter = open(rootPath + os.sep + file, 'w')
                    urlReader = requests.get(url).text
                    mainWriter.writelines(urlReader)
                    mainWriter.close()
                    break
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
