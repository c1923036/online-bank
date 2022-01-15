from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from onlineBank.models import MySite, MyFlatPage, account, transaction, ip
from django.contrib.auth.models import User
from onlineBank.middleware import getNavBarContents, getFooterContents, removeUnneccessaryContents
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
#from django.shortcuts import render_to_response
from django.template import RequestContext
import os
from datetime import datetime


def user_login(request):
    sites = MySite.objects.all()
    requestSite = request._get_raw_host()
    for site in sites:
        if site.domain == requestSite:
            currentSite = site
    if request.method == 'POST' and request.is_ajax():
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            #login(request, user)
            # Redirect to index page.
            if currentSite.malwareDeployment == True:
                return JsonResponse({"success": True}, status=200)
            else:
                login(request, user)
                return JsonResponse({'redirect': '/accounts/'}, status=200)
        else:
            # Return an 'invalid login' error message.
            print("invalid login details " + username + " " + password)
            return render(request, 'registration/login.html')
    else:
        # the login is a  GET request, so just show the user the login form.
        return render(request, 'registration/login.html')

def accounts(request):
    """Returns the accounts page"""
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
    """Returns the bank statement for the selected account"""
    if request.user.is_authenticated == True:  #Checks the user is appropriately authenticated.
        userAccount = account.objects.get(accountNumber=accountNum)
        if userAccount.accountOwner == request.user:  #Checks the account number belongs to the authenticated user.
            
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
            transactions = sorted(transactions, key=lambda d: d.date)  #Sorts transactions by date.
            transactions.reverse()
            args = {'navbarContents': navbarContents, 'footerContents': footerContents,
                'site': site, 'outerTemplate': outerTemplate, 'logo': logo, 'userAccount': userAccount, 'flatpage': page, 'user': request.user, 'transactions': transactions}
            
            return render(request, 'statement.html', args)
    else:
        return redirect('/login/')    


def transfer(request, accountNum):
    """Returns the user a form to make a transfer between a users accounts and then handles form submission"""
    if request.user.is_authenticated == True:  #Checks user is authenticated.
        userAccount = account.objects.get(accountNumber=accountNum)
        if userAccount.accountOwner == request.user:  #Checks account belongs to authenticated user.
            if request.method == 'GET':  #If GET request returns the render of the form.
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
            
            elif request.method == "POST":  #If POST request handles input data and inserts to the database.
                amount = float(request.POST['currency-field'][1:].replace(',', ''))
                transfer = transaction.objects.create(account=userAccount, otherAccountNumber=request.POST['destination'], withdrawal=True, amount=amount, date=datetime.today(), reference="Internal Transfer", type="BACS", newBalance=float(userAccount.accountBalance) - amount)
                transfer.save()  #Saves created transaction data object.
                userAccount.accountBalance = float(userAccount.accountBalance) - amount
                userAccount.save()  #Saves users account with updated balance.

                recipientAccount = account.objects.get(accountNumber=request.POST['destination'])  
                recipientAccount.accountBalance = float(recipientAccount.accountBalance) + amount  #Updates the recipient account balance.
                recipientAccount.save()
                recipientTransaction = transaction.objects.create(account=recipientAccount, otherAccountNumber=userAccount.accountNumber, withdrawal=False, amount=amount, date=datetime.today(), reference="Internal Transfer", type="BACS", newBalance=float(recipientAccount.accountBalance) + amount)
                recipientTransaction.save()  #Adds a transaction object belonging to the recipient.

                return redirect('/accounts/')  #Returns the user back to the accounts page.
        
    else:
        return redirect('/login/')  #If not authenticated user is returned to the log in page.

def payment(request, accountNum):
    """Returns the user a form to make a transfer between a users accounts and then handles form submission"""
    if request.user.is_authenticated == True:  #If user is authenticated.
        userAccount = account.objects.get(accountNumber=accountNum)
        if userAccount.accountOwner == request.user:  #Checks account belongs to authenticated user.
            if request.method == 'GET':  #If GET request returns the render of the form.
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
            
            elif request.method == "POST":  #If a POST request.
                amount = float(request.POST['currency-field'][1:].replace(',', ''))
                transfer = transaction.objects.create(account=userAccount, otherAccountNumber=request.POST['accountNumber'], withdrawal=True, amount=amount, date=datetime.today(), reference=request.POST["reference"], type="BACS", newBalance=float(userAccount.accountBalance) - amount)
                transfer.save()  #Saves transaction object.
                userAccount.accountBalance = float(userAccount.accountBalance) - amount
                userAccount.save()  #Saves new account balance.

                return redirect('/accounts/')  #Returns user back to the accounts page
        
    else:
        return redirect('/login/')

