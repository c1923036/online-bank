from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from onlineBank.models import MySite, MyFlatPage, account
from onlineBank.middleware import getNavBarContents, getFooterContents, removeUnneccessaryContents
import os


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
        navbarContents = getNavBarContents(pages)
        footerContents = getFooterContents(pages)
        removeUnneccessaryContents(navbarContents, request.user.is_authenticated)
        
        accounts = account.objects.all()
        userAccounts = []
        for bankAccount in accounts:
            if bankAccount.accountOwner.username == request.user.username:
                userAccounts.append(bankAccount)

        args = {'navbarContents': navbarContents, 'footerContents': footerContents,
                'site': site, 'outerTemplate': outerTemplate, 'logo': logo, 'userAccounts': userAccounts}

        return render(request, 'accounts.html', args)

    else:
        return redirect('/login/')
