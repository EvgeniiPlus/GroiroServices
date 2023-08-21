from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('daily_report/', dailyReport, name='dailyReport'),
    path('choose_structure/', chooseStructure, name='chooseStructure'),
    path('list_reports/<int:pk>', listReports, name='listReports'),
    path('my_reports/', myReports, name='myReports'),
    path('my_services/', myServices, name='myServices'),
]
