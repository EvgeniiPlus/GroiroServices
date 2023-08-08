from django.contrib import admin
from .models import *


class ServicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'structure', 'price')
    list_display_links = ('id', 'name')
    search_fields = ('name', )
    list_editable = ('price',)
    list_filter = ('structure',)


class StructuresAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'employee')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'employee')
    list_editable = ('employee',)


class RolesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name')
    search_fields = ('name',)



class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'surname', 'name', 'role')
    list_display_links = ('id', 'surname', 'name')
    search_fields = ('surname', 'name')
    list_editable = ('role',)
    list_filter = ('role',)


class ReportsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'service', 'amount', 'sum', 'date_create', 'date_edit')
    list_display_links = ('id', 'date', 'service')
    list_filter = ('date', 'service', 'date_create')


admin.site.register(Services, ServicesAdmin)
admin.site.register(Structures, StructuresAdmin)
admin.site.register(Roles, RolesAdmin)
admin.site.register(Users, UsersAdmin)
admin.site.register(Reports, ReportsAdmin)
