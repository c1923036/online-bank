import names
import os


def parseCSV():
    splitdata = []
    dictData = []
    dir = os.getcwd()
    csvfile = open('onlineBank/dataset/transactionData.csv', 'r').readlines()
    for i in range(1,len(csvfile)):
        splitLine = csvfile[i].split(",")
        splitdata.append(splitLine)
        dataObj = {}
        dataObj["recipient"] = splitLine[3]
        dataObj["type"] = splitLine[4]
        dataObj["amount"] = splitLine[5]
        dataObj["date"] = splitLine[6]
        if splitLine[7] == "Negative":
            dataObj["withdrawal"] = True
        else:
            dataObj["withdrawal"] = False
        dictData.append(dataObj)
        

    return dictData

if __name__ == '__main__':
    parseCSV()