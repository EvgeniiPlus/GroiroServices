from django.contrib import admin
from .models import *


class ServicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'structure', 'price')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_editable = ('structure', 'price')
    list_filter = ('structure', 'name', 'price')


class StructuresAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'employee')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'employee')
    list_editable = ('employee', )
    list_filter = ('structure', 'name', 'price')


admin.site.register(Services, ServicesAdmin)
