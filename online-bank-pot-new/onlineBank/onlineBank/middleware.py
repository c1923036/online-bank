from onlineBank.models import MyFlatPage, outerTemplate
from onlineBank.models import MySite
from onlineBank.settings import NAVBAR_CONSTANTS
import os
from django.shortcuts import render


class myFlatpages:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            pages = MyFlatPage.objects.all()
            for page in pages:
                if page.url == request.path and (page.registration_required != True or request.user.is_authenticated == True):
                    site = page.appearOnSites
                    if page.template != None:
                        innerTemplate = page.template.file.path
                    else:
                        innerTemplate = "flatpages/default.html"
                    if site.template != None:
                        outerTemplate = site.template.file.path
                    else:
                        outerTemplate = "template.html"
                    if site.logo != None:
                        logo = os.path.relpath(
                            site.logo.file.url, '/onlineBank/static')
                    else:
                        logo = None

                    navbarContents = getNavBarContents(pages)
                    footerContents = getFooterContents(pages)

                    navbarContents = removeUnneccessaryContents(navbarContents, request.user.is_authenticated)

                    args = {'flatpage': page, 'navbarContents': navbarContents, 'footerContents': footerContents,
                            'site': site, 'outerTemplate': outerTemplate, 'logo': logo}
                    response = render(request, innerTemplate, args)
        return response


def getNavBarContents(pages):
    navbarContents = []
    navbarContents += NAVBAR_CONSTANTS
    for page in pages:
        if page.appearOnNavbar == True:
            navbarContents.append({'name': page.title, 'url': page.url})
    return navbarContents


def getFooterContents(pages):
    footerContents = []
    for page in pages:
        if page.appearOnNavbar == True:
            footerContents.append({'name': page.title, 'url': page.url})
    return footerContents

def removeUnneccessaryContents(navbarContents, loggedIn):
    for i in range(0, len(navbarContents)):
        if loggedIn == True and navbarContents[i]['url'] == "/login":
            navbarContents.pop(i)
            return navbarContents
        elif loggedIn == False and navbarContents[i]['url'] == "/logout":
            navbarContents.pop(i)
            return navbarContents
    return navbarContents