from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *


@admin.register(Police_victim,Victims)
@admin.register(News)
class InfluencerAdmin(ImportExportModelAdmin):
    pass
