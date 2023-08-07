from django.contrib import admin
from .models import *


class ServicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'structure', 'price')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_editable = ('structure', 'price')
    list_filter = ('structure', 'name', 'price')


class StructuresAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'employee')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'employee')
    list_editable = ('employee',)
    list_filter = ('name', 'employee')


class RolesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name')
    search_fields = ('name', )
    list_filter = ('name', )


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'surname', 'name', 'role')
    list_display_links = ('id', 'surname', 'name')
    search_fields = ('surname', 'name')
    list_editable = ('role', )
    list_filter = ('role', )


admin.site.register(Services, ServicesAdmin)
admin.site.register(Structures, StructuresAdmin)
admin.site.register(Roles, RolesAdmin)
admin.site.register(Users, UsersAdmin)
