import numpy
def getBoxPlotList (dataList):
    xq1 = numpy.percentile(dataList, 25)
    xq3 = numpy.percentile(dataList, 75)
    iqr = xq3 - xq1
    uprBound = xq3 + 1.5 * iqr
    lwrBound = xq1 - 1.5 * iqr
    newDataList = []
    outlier = []
    for i in dataList:
        value = i
        if i > uprBound:
            value = uprBound
            outlier.append(i)
        elif i < lwrBound:
            value = lwrBound
            outlier.append(i)
        else:
            newDataList.append(i)
    print('Box plot found outlier count : {}'.format(len(outlier)))
    return newDataList

def getMeanMedianErrror(dataList):
    dataMean = numpy.mean(dataList)
    dataMedian = numpy.median(dataList)
    dataError = abs(dataMean - dataMedian)
    dataSet = { 'mean' : dataMean, 'median' : dataMedian, 'error' : dataError }
    print(dataSet)
    return dataSet

