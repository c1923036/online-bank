import names
import os
import random
from datetime import datetime, timedelta
from .models import account, transaction

incomeSource = "Warwick Intelligent Manufacturing Limited"
monthlySalary = 3288

def generateMaleNames():
    name = "Mr "
    name += names.get_full_name(gender='male')
    return name

def generateFemaleNames():
    name = "Ms "
    name += names.get_full_name(gender='female')
    return name

def parseCSV():
    splitdata = []
    randomNames = [generateMaleNames() for i in range(20)]
    randomNames += [generateFemaleNames() for i in range(20)]
    dictData = []
    divisors = [8, 10, 11, 12, 13, 14]
    
    foodRetail = open('onlineBank/dataset/foodRetail.csv', 'r').read().split(',')
    csvfile = open('onlineBank/dataset/transactionData.csv', 'r').readlines()
    for i in range(1,len(csvfile)):
        splitLine = csvfile[i].split(",")
        splitdata.append(splitLine)
        dataObj = {}
        dataObj["recipient"] = splitLine[3]
        dataObj["type"] = splitLine[4]
        try:
            dataObj["amount"] = int(splitLine[5])
        except:
            continue
        if splitLine[7] == "Negative\n":
            dataObj["withdrawal"] = True
        else:
            dataObj["withdrawal"] = False

        if dataObj["type"] == "Translation":
            dataObj["recipient"] = randomNames[random.randint(0, len(randomNames)-1)]
            dataObj["type"] = "Transfer"
        if dataObj["type"] == "Subscription":
            dataObj["amount"] = dataObj["amount"]/16
        else:
            dataObj["amount"] = dataObj["amount"]/random.choice(divisors)
        
        if dataObj["type"] == "Purchase" and dataObj["recipient"] == "":
            dataObj["recipient"] = foodRetail[random.randint(0, len(foodRetail)-1)]
        
        if dataObj["type"] == "Replenishment":
            dataObj["type"] = "BACS"
            dataObj["recipient"] = incomeSource
            dataObj["amount"] = monthlySalary

        dictData.append(dataObj)
        

    return dictData

def createTransactions():
    transactionData = parseCSV()
    finalData = []
    dates = []
    period = 1051200 #Minutes (2 Years)
    numberOfTransactions = 500
    for i in range(numberOfTransactions):
        timeOffset = random.randint(0, period)
        dates.append(str(datetime.today() - timedelta(minutes=timeOffset)))
    dates.sort()
    total = 0
    for i in range(numberOfTransactions):    
        transaction = {}
        transaction["datetime"] = dates[i]
        transaction["recipient"] = transactionData[i]["recipient"]
        transaction["type"] = transactionData[i]["type"]
        transaction["amount"] = round(transactionData[i]["amount"], 2)
        transaction["withdrawal"] = transactionData[i]["withdrawal"]
        if transaction["withdrawal"] == True:
            total -= transaction["amount"]
        else:
            total += transaction["amount"]


        finalData.append(transaction)

    return finalData

def createBankStatement(accountToUse):
    transactions = createTransactions()
    accounts = account.objects.all()
    
    balanceAfterLastTransaction = float(accountToUse.accountBalance)
    for i in range(len(transactions)-1, 0, -1):
        newTransaction = transaction()
        newTransaction.account=accountToUse
        newTransaction.withdrawal=transactions[i]["withdrawal"]
        newTransaction.amount=transactions[i]["amount"]
        newTransaction.date=transactions[i]["datetime"]
        newTransaction.reference=transactions[i]["recipient"]
        newTransaction.type=transactions[i]["type"]
        newTransaction.newBalance=balanceAfterLastTransaction
        if transactions[i]["withdrawal"] == True:
            balanceAfterLastTransaction = balanceAfterLastTransaction+transactions[i]["amount"]
        else:
            balanceAfterLastTransaction = balanceAfterLastTransaction-transactions[i]["amount"]
        #newTransaction = transaction.objects.create(account=accountToUse, otherAccountNumber='', withdrawal=transactions[i]["withdrawal"], amount=transactions[i]["amount"], date=transactions[i]["datetime"], reference=transactions[i]["recipient"], type=transactions[i]["type"], newBalance=balanceAfterLastTransaction-transactions[i]["amount"])
        newTransaction.save()

if __name__ == '__main__':
    createTransactions()