from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.forms import FlatpageForm
from django.contrib.flatpages.models import FlatPage
from django.forms.widgets import TextInput

from .models import MyFlatPage

class ExtendedFlatPageForm(FlatpageForm):
    class Meta:
        model = MyFlatPage
        fields = '__all__'
        widgets = {
            'header_colour': TextInput(attrs={'type': 'color'}),
            'footer_colour': TextInput(attrs={'type': 'color'}),
            'page_colour': TextInput(attrs={'type': 'color'}),
            'margin_colour': TextInput(attrs={'type': 'color'}),
        }

class ExtendedFlatPageAdmin(FlatPageAdmin):
    form = ExtendedFlatPageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites', 'appearOnNavbar', 'appearOnFooter', 'header_colour', 'footer_colour', 'page_colour', 'margin_colour')}),
    )

admin.site.unregister(FlatPage)
admin.site.register(MyFlatPage, ExtendedFlatPageAdmin)