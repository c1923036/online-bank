from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.forms import FlatpageForm
from django.contrib.flatpages.models import FlatPage

from .models import MyFlatPage

class ExtendedFlatPageForm(FlatpageForm):
    class Meta:
        model = MyFlatPage
        fields = '__all__'

class ExtendedFlatPageAdmin(FlatPageAdmin):
    form = ExtendedFlatPageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites', 'appearOnNavbar')}),
    )

admin.site.unregister(FlatPage)
admin.site.register(MyFlatPage, ExtendedFlatPageAdmin)