from onlineBank.models import MyFlatPage
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
                    navbarContents = getNavBarContents(pages)
                    args = {'flatpage': page, 'navbarContents': navbarContents}
                    response = render(request, 'flatpages/default.html', args)
        return response


def getNavBarContents(pages):
    navbarContents = []
    for page in pages:
        if page.appearOnNavbar == True:
            navbarContents.append({'name': page.title, 'url': page.url})
    return navbarContents