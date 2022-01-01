from django.contrib import admin
from django.db import models
from django.contrib.flatpages.models import FlatPage

class MyFlatPage(FlatPage):
    appearOnNavbar = models.BooleanField(default=False)
    appearOnFooter = models.BooleanField(default=False)

    


#admin.site.register(MyFlatPage)
#admin.site.unregister(FlatPage)