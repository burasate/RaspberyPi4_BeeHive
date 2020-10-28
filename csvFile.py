import csv,os

#rootPath = 'D:/GoogleDrive/Documents/2020/Beehive_Iot/BeehivePy'
rootPath = os.path.dirname(os.path.abspath(__file__))
dataPath = rootPath+'/data'

def create (filePath, header):
    tableList = [list(header)]
    with open(filePath, 'x',newline='') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        writer.writerows(tableList)
        outfile.close()

def addRow (filePath, column):
    tableList = []
    with open(filePath, 'r',newline='') as readfile:
        for row in csv.reader(readfile):
            tableList.append(row)
        readfile.close()
    #Add Row
    tableList.append(column)

    with open(filePath, 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        writer.writerows(tableList)
        outfile.close()

def getAll (filePath):
    print(filePath)
    tableList = []
    index = 0
    print('Reading {}'.format(filePath))
    with open(filePath, 'r',newline='') as readfile:
        for row in csv.reader(readfile):
            tableList.append(row)
            if index == 0:
                #print('Header Count {}'.format(len(row)))
                pass
            print ('{:04} {}'.format(index,row))
            index = index+1
        readfile.close()
    return tableList

def getRow (filePath, findIndex=0):
    index = 0
    print('Getting Row In {}  Index {}'.format(filePath,int(findIndex)))
    with open(filePath, 'r', newline='') as readfile:
        for row in csv.reader(readfile):
            if index == findIndex:
                print('{:04} {}'.format(index, row))
                return row
            index = index + 1
        readfile.close()

def getRowCount (filePath):
    index = 0
    print('Reading Row Count In {}'.format(filePath))
    with open(filePath, 'r', newline='') as readfile:
        print(len(readfile))
        readfile.close()

def deleteRow (filePath, findIndex):
    tableList = []
    index = 0
    with open(filePath, 'r', newline='') as readfile:
        for row in csv.reader(readfile):
            if index != findIndex:
                tableList.append(row)
            index = index + 1
        readfile.close()

    with open(filePath, 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        writer.writerows(tableList)
        outfile.close()

if __name__ == '__main__':
    #"""
    header = ['Date','Name','Weight','Temperature','Humidity']
    column = ['2020-10-11','BRSHive101','10','38.5','60']
    path = 'C:/Users/DEX3D_I7/Desktop/ttt.csv'
    try:
        create(path, header)
    except:
        pass
    finally:
        addRow(path, column)
        #csvPrintRow(path,2)
        getAll(path)
    #"""

