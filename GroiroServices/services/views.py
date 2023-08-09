from datetime import datetime

from django.shortcuts import render

from .models import *
from django.http import HttpResponse, HttpResponseNotFound, StreamingHttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, CreateView

# Create your views here.

menu = [{'title': 'Главная', 'url_name': 'home', 'role': ['Администратор', 'Оператор', 'Экономист']},
        {'title': 'Создать отчет', 'url_name': 'dailyReport', 'role': ['Оператор']},
        {'title': 'Просмотреть отчеты', 'url_name': 'viewReport', 'role': ['Администратор', 'Экономист']},

        ]


def home(request):
    context = {
        'menu': menu,
        'title': 'ГрОИРО. Услуги',
        'services': Services.objects.all(),
        'userRole': str(Users.objects.get(user=request.user).role)
    }
    return render(request, 'services/index.html', context)


def dailyReport(request):
    context = {
        'menu': menu,
        'title': 'ГрОИРО. Услуги',
        'services': Services.objects.filter(structure=Structures.objects.get(employee=Users.objects.get(user=request.user))),
        'structure': Structures.objects.filter(employee=Users.objects.get(user=request.user))[0],
        'current_date': datetime.now(),
        'userRole': str(Users.objects.get(user=request.user).role)
    }

    if request.method == 'POST':
        date = request.POST.get('service_date')
        service_id_list = request.POST.getlist('service_id')
        service_count_list = request.POST.getlist('service_count')
        # print(f'{date} \n{service_id_list} \n{service_count_list}')

        for i in range(len(service_id_list)):
            if int(service_count_list[i]) != 0:
                Reports.objects.create(
                    date=date,
                    service=Services.objects.get(pk=service_id_list[i]),
                    amount=service_count_list[i],
                    sum=round(int(service_count_list[i]) *
                              Services.objects.filter(pk=service_id_list[i])[0].price, 2)
                )
            else:
                continue

        return redirect('/')

    return render(request, 'services/DailyReport.html', context)

def viewReport(request):
    context = {
        'menu': menu,
        'title': 'ГрОИРО. Услуги',
        'structures': Structures.objects.all(),
        'current_date': datetime.now(),
        'userRole': str(Users.objects.get(user=request.user).role)
    }

    return render(request, 'services/viewReport.html', context)