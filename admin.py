from django.contrib import admin
from import_export.admin import ImportExportMixin
from import_export import resources
from .models import *


class Oi00Resource(resources.ModelResource):
    class Meta:
        model = Oi00
        exclude = ('id', )

class Oi00Admin(ImportExportMixin, admin.ModelAdmin):
    pass

admin.site.register(Oi00, Oi00Admin)
