import json,os,gSheet,lineNotify

rootPath = os.path.dirname(os.path.abspath(__file__))
dataPath = rootPath+'/data'
configPath = dataPath + '/brsHiveInfo.json'
configJson = json.load(open(configPath))

inputId = input('Enter BRSHive Id Name: ')
inputOwner = input('Enter BRSHive Owner: ')
inputDesc = input('Enter BRSHive Description: ')

print('Sending Request...')
configData = gSheet.loadConfigData(inputId)
if configData == None:
    configJson['idName'] = inputId
    configJson['description'] = inputDesc
    configJson['owner'] = inputOwner
    json.dump(configJson, open(configPath, 'w'), indent=4)

    gSheet.addRow('Config',[inputId])
    gSheet.updateConfigValue(inputId, 'description', inputDesc)
    gSheet.updateConfigValue(inputId, 'owner', inputOwner)
    for colName in configJson['config']:
        print ('sending config data.. {}  {}'.format(colName,configJson['config'][colName]))
        gSheet.updateConfigValue(inputId, 'config_'+colName, configJson['config'][colName])

    finishText = '{} has been registered\nPlease check on your database'.format(inputId)
    print(finishText)
    lineNotify.sendNotifyMassage(finishText)

