from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from onlineBank.models import MySite, MyFlatPage, account, transaction
from django.contrib.auth.models import User
from onlineBank.middleware import getNavBarContents, getFooterContents, removeUnneccessaryContents
import os
from datetime import datetime


#def login(request):
#    if request.method == 'POST':
#        username = request.POST['username']
#        password = request.POST['password']
#        user = authenticate(request, username=username, password=password)
#        if user is not None:
#            login(request, user)
#            redirect('/accounts/')
#    elif request.method == 'GET':
#        sites = MySite.objects.all()
#        requestSite = request._get_raw_host()
#        for site in sites:
#            if site.domain == requestSite:
#                currentSite = site
#        if currentSite == None:
#            return
#        if site.template != None:
#            outerTemplate = site.template.file.path
#        else:
#            outerTemplate = "template.html"
#        if site.logo != None:
#            logo = os.path.relpath(
#                site.logo.file.url, '/onlineBank/static')
#        else:
#            logo = None
#        
#        pages = MyFlatPage.objects.all()
#        navbarContents = getNavBarContents(pages)
#        footerContents = getFooterContents(pages)
#
#        args = {'navbarContents': navbarContents, 'footerContents': footerContents,
#                'site': site, 'outerTemplate': outerTemplate, 'logo': logo}
#
#        return render(request, 'login.html', args)


def accounts(request):
    
    if request.user.is_authenticated == True:
        
        sites = MySite.objects.all()
        requestSite = request._get_raw_host()
        for site in sites:
            if site.domain == requestSite:
                currentSite = site
        if currentSite == None:
            return
        if site.template != None:
            outerTemplate = site.template.file.path
        else:
            outerTemplate = "template.html"
        if site.logo != None:
            logo = os.path.relpath(
                site.logo.file.url, '/onlineBank/static')
        else:
            logo = None

        pages = MyFlatPage.objects.all()
        #navbarContents = getNavBarContents(pages)
        footerContents = getFooterContents(pages)
        #removeUnneccessaryContents(navbarContents, request.user.is_authenticated)
        
        accounts = account.objects.all()
        userAccounts = []
        for bankAccount in accounts:
            if bankAccount.accountOwner.username == request.user.username:
                userAccounts.append(bankAccount)

        user = userAccounts[0].accountOwner

        page = {}
        page["page_colour"] = "#FFFFFF"

        navbarContents = []
        args = {'navbarContents': navbarContents, 'footerContents': footerContents,
                'site': site, 'outerTemplate': outerTemplate, 'logo': logo, 'userAccounts': userAccounts, 'flatpage': page, 'user': user}

        return render(request, 'accounts.html', args)

    else:
        return redirect('/login/')


def statement(request, accountNum):
    if request.user.is_authenticated == True:
        userAccount = account.objects.get(accountNumber=accountNum)
        if userAccount.accountOwner == request.user:
            
            sites = MySite.objects.all()
            requestSite = request._get_raw_host()
            for site in sites:
                if site.domain == requestSite:
                    currentSite = site
            if currentSite == None:
                return
            if site.template != None:
                outerTemplate = site.template.file.path
            else:
                outerTemplate = "template.html"
            if site.logo != None:
                logo = os.path.relpath(
                    site.logo.file.url, '/onlineBank/static')
            else:
                logo = None

            pages = MyFlatPage.objects.all()
            #navbarContents = getNavBarContents(pages)
            footerContents = getFooterContents(pages)
            #removeUnneccessaryContents(navbarContents, request.user.is_authenticated)
            page = {}
            page["page_colour"] = "#FFFFFF"

            navbarContents = []

            transactions = transaction.objects.filter(account=userAccount)
            transactions = list(transactions)
            transactions = sorted(transactions, key=lambda d: d.date)
            transactions.reverse()
            args = {'navbarContents': navbarContents, 'footerContents': footerContents,
                'site': site, 'outerTemplate': outerTemplate, 'logo': logo, 'userAccount': userAccount, 'flatpage': page, 'user': request.user, 'transactions': transactions}
            
            return render(request, 'statement.html', args)
    else:
        return redirect('/login/')    


def transfer(request, accountNum):
    if request.user.is_authenticated == True:
        userAccount = account.objects.get(accountNumber=accountNum)
        if userAccount.accountOwner == request.user:
            if request.method == 'GET':
                sites = MySite.objects.all()
                requestSite = request._get_raw_host()
                for site in sites:
                    if site.domain == requestSite:
                        currentSite = site
                if currentSite == None:
                    return
                if site.template != None:
                    outerTemplate = site.template.file.path
                else:
                    outerTemplate = "template.html"
                if site.logo != None:
                    logo = os.path.relpath(
                        site.logo.file.url, '/onlineBank/static')
                else:
                    logo = None

                pages = MyFlatPage.objects.all()
                #navbarContents = getNavBarContents(pages)
                footerContents = getFooterContents(pages)
                #removeUnneccessaryContents(navbarContents, request.user.is_authenticated)
                page = {}
                page["page_colour"] = "#FFFFFF"

                navbarContents = []

                userAccounts = []
                accounts = account.objects.all()
                for bankAccount in accounts:
                    if bankAccount.accountOwner.username == request.user.username and bankAccount.accountNumber != userAccount.accountNumber:
                        userAccounts.append(bankAccount)


                args = {'navbarContents': navbarContents, 'footerContents': footerContents,
                    'site': site, 'outerTemplate': outerTemplate, 'logo': logo, 'payingAccount': userAccount, 'flatpage': page, 'user': request.user, 'userAccounts': userAccounts}
                
                return render(request, 'transfer.html', args)
            
            elif request.method == "POST":
                if request.user.is_authenticated == True:
                    userAccount = account.objects.get(accountNumber=accountNum)
                    if userAccount.accountOwner == request.user:
                        amount = float(request.POST['currency-field'][1:].replace(',', ''))
                        transfer = transaction.objects.create(account=userAccount, otherAccountNumber=request.POST['destination'], withdrawal=True, amount=amount, date=datetime.today(), reference="Internal Transfer", type="BACS", newBalance=float(userAccount.accountBalance) - amount)
                        transfer.save()
                        userAccount.accountBalance = float(userAccount.accountBalance) - amount
                        userAccount.save()

                        recipientAccount = account.objects.get(accountNumber=request.POST['destination'])
                        recipientAccount.accountBalance = float(recipientAccount.accountBalance) + amount
                        recipientAccount.save()
                        recipientTransaction = transaction.objects.create(account=recipientAccount, otherAccountNumber=userAccount.accountNumber, withdrawal=False, amount=amount, date=datetime.today(), reference="Internal Transfer", type="BACS", newBalance=float(recipientAccount.accountBalance) + amount)
                        recipientTransaction.save()

                        return redirect('/accounts/')
        
    else:
        return redirect('/login/')

def payment(request, accountNum):
    if request.user.is_authenticated == True:
        userAccount = account.objects.get(accountNumber=accountNum)
        if userAccount.accountOwner == request.user:
            if request.method == 'GET':
                sites = MySite.objects.all()
                requestSite = request._get_raw_host()
                for site in sites:
                    if site.domain == requestSite:
                        currentSite = site
                if currentSite == None:
                    return
                if site.template != None:
                    outerTemplate = site.template.file.path
                else:
                    outerTemplate = "template.html"
                if site.logo != None:
                    logo = os.path.relpath(
                        site.logo.file.url, '/onlineBank/static')
                else:
                    logo = None

                pages = MyFlatPage.objects.all()
                #navbarContents = getNavBarContents(pages)
                footerContents = getFooterContents(pages)
                #removeUnneccessaryContents(navbarContents, request.user.is_authenticated)
                page = {}
                page["page_colour"] = "#FFFFFF"

                navbarContents = []

                userAccounts = []
                accounts = account.objects.all()
                for bankAccount in accounts:
                    if bankAccount.accountOwner.username == request.user.username and bankAccount.accountNumber != userAccount.accountNumber:
                        userAccounts.append(bankAccount)


                args = {'navbarContents': navbarContents, 'footerContents': footerContents,
                    'site': site, 'outerTemplate': outerTemplate, 'logo': logo, 'payingAccount': userAccount, 'flatpage': page, 'user': request.user, 'userAccounts': userAccounts}
                
                return render(request, 'payment.html', args)
            
            elif request.method == "POST":
                if request.user.is_authenticated == True:
                    userAccount = account.objects.get(accountNumber=accountNum)
                    if userAccount.accountOwner == request.user:
                        amount = float(request.POST['currency-field'][1:].replace(',', ''))
                        transfer = transaction.objects.create(account=userAccount, otherAccountNumber=request.POST['accountNumber'], withdrawal=True, amount=amount, date=datetime.today(), reference=request.POST["reference"], type="BACS", newBalance=float(userAccount.accountBalance) - amount)
                        transfer.save()
                        userAccount.accountBalance = float(userAccount.accountBalance) - amount
                        userAccount.save()

                        return redirect('/accounts/')
        
    else:
        return redirect('/login/')