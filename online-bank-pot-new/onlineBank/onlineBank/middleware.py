from onlineBank.models import MyFlatPage, outerTemplate
from onlineBank.models import MySite
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
                if page.url == request.path:
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
                        logo = os.path.relpath(site.logo.file.url, '/onlineBank/static')
                    else:
                        logo = None

                    navbarContents = getNavBarContents(pages)
                    footerContents = getFooterContents(pages)
                    args = {'flatpage': page, 'navbarContents': navbarContents, 'footerContents': footerContents, 'site': site, 'outerTemplate': outerTemplate, 'logo': logo}
                    response = render(request, innerTemplate, args)
        return response


def getNavBarContents(pages):
    navbarContents = []
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