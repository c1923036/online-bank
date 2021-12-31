from django.contrib import admin
from django.db import models
from django.contrib.flatpages.models import FlatPage

class navbarContent(models.Model):
    page = models.OneToOneField(
        FlatPage,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Page Name",
    )

    appearOnNavbar = models.BooleanField(default=False)

admin.site.register(navbarContent)
