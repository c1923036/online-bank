import names
import os


def parseCSV():
    splitdata = []
    dictData = []
    dir = os.getcwd()
    csvfile = open('onlineBank/dataset/transactionData.csv', 'r').readlines()
    for i in range(1,len(csvfile)):
        splitdata.append(csvfile[i].split(","))
        dataObj = {}
        

    return

if __name__ == '__main__':
    parseCSV()