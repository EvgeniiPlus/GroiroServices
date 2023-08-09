from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('daily_report/', dailyReport, name='dailyReport'),
    path('view_report/', viewReport, name='viewReport'),
]