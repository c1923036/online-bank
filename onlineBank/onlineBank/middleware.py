from onlineBank.models import MyFlatPage
from onlineBank.monitoring import recordAccess
from django.shortcuts import render
from onlineBank.arguments import createArgs


class myFlatpages:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Returns flatpage render if necessary

        If the current response is due to be a 404 error the request is checked to see if it is for one of the user created flatpages.  If this is the case the page will be rendered.
        """
        recordAccess(request)
        response = self.get_response(request)
        if response.status_code == 404:  # Checks for 404 error.
            pages = MyFlatPage.objects.all()
            for page in pages:
                # Checks if the page has been rendered. Also checks if authentication is necessary, if so authentication is checked.
                if page.url == request.path and (page.registration_required != True or request.user.is_authenticated == True):
                    site = page.appearOnSites  # Gets the page's site.
                    if page.template != None:
                        innerTemplate = page.template.file.path
                    else:
                        # Default inner template value assigned if null.
                        innerTemplate = "flatpages/default.html"
                    args = createArgs(request)
                    if args == None:
                        response = render(request, 'noSiteTemplate.html')
                    else:
                        response = render(request, innerTemplate, args)
        return response


def removeUnneccessaryContents(navbarContents, loggedIn):
    """Returns navbar contents minus the login or logout object depending on if the user is logged in or logged out"""
    for i in range(0, len(navbarContents)):
        if loggedIn == True and navbarContents[i]['url'] == "/login":
            navbarContents.pop(i)
            return navbarContents
        elif loggedIn == False and navbarContents[i]['url'] == "/logout":
            navbarContents.pop(i)
            return navbarContents
    return navbarContents
