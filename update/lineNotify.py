import json,requests,os

rootPath = os.path.dirname(os.path.abspath(__file__))
dataPath = rootPath+'/data'
configPath = dataPath + '/brsHiveInfo.json'
configJson = json.load(open(configPath))

url = 'https://notify-api.line.me/api/notify'
token = configJson['config']['lineToken']
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

def sendNotifyMassage (text):
    print('Sending Massage')
    r = requests.post(url, headers=headers , data = {'message':'\n'+text})
    print (r.text)

def sendNotifyImageMsg (imagePath,text='send image'):
    print('Sending Image {}'.format(imagePath))
    r = requests.post(url, headers=headers ,data = {'message': '\n'+text}, files = {'imageFile':open(imagePath,'rb')})
    print (r.text)

if __name__=='__main__':
    #sendNotifyMassage('test')
    sendNotifyImageMsg('C:/Users/DEX3D_I7/Pictures/UglyDolls2_1.mp4_snapshot_01.17.998.jpg')
    pass