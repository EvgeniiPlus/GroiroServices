from datetime import datetime,tzinfo, timezone

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import *
from django.http import HttpResponse, HttpResponseNotFound, StreamingHttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, CreateView

import pandas


# Create your views here.

menu = [{'title': 'Главная', 'url_name': 'home', 'role': ['Администратор', 'Оператор', 'Экономист']},
        {'title': 'Создать отчет', 'url_name': 'dailyReport', 'role': ['Оператор']},
        {'title': 'Отчеты', 'url_name': 'chooseStructure', 'role': ['Администратор', 'Экономист']},
        ]

userMenu = [{'title': 'Админ-панель', 'url_name': 'admin:index', 'role': ['Администратор']},
            {'title': 'Мои отчеты', 'url_name': 'myReports', 'role': ['Оператор']},
            {'title': 'Мои услуги', 'url_name': 'myServices', 'role': ['Оператор']},
            ]

def home(request):
    context = {
        'menu': menu,
        'userMenu': userMenu,
        'title': 'ГрОИРО. Услуги',

        'structures': Structures.objects.all()
    }

    if request.user.is_authenticated:
        context['userRole'] = str(Users.objects.get(user=request.user).role)

    return render(request, 'services/index.html', context)


def dailyReport(request):
    context = {
        'menu': menu,
        'userMenu': userMenu,
        'title': 'Ежедневный отчет',
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
                    structure=Structures.objects.filter(employee=Users.objects.get(user=request.user))[0],
                    amount=service_count_list[i],
                    sum=round(int(service_count_list[i]) *
                              Services.objects.filter(pk=service_id_list[i])[0].price, 2)
                )
            else:
                continue

        return redirect('/')

    return render(request, 'services/DailyReport.html', context)

def chooseStructure(request):
    context = {
        'menu': menu,
        'userMenu': userMenu,
        'title': 'Выбор структуры',
        'structures': Structures.objects.all(),
        'userRole': str(Users.objects.get(user=request.user).role)
    }

    return render(request, 'services/chooseStructure.html', context)

def listReports(request, pk):
    context = {
        'menu': menu,
        'userMenu': userMenu,
        'title': 'Отчеты',
        'structure': Structures.objects.get(pk=pk),
        'services': Services.objects.filter(structure=Structures.objects.get(pk=pk)),
        'userRole': str(Users.objects.get(user=request.user).role),
        'reports': Reports.objects.filter(structure=pk).order_by('-date')
    }

    if request.method == 'POST':
        date_start = str(request.POST.get('date_start'))
        date_finish = str(request.POST.get('date_finish'))
        service = request.POST.get('service')
        if date_start and date_finish != '':
            if service == 'all':
                reports = Reports.objects.filter(structure=Structures.objects.get(pk=pk),
                                                 date__gte=date_start,
                                                 date__lte=date_finish)
            else:
                reports = Reports.objects.filter(service__name=service,
                                                 date__gte=date_start,
                                                 date__lte=date_finish)
        else:
            if service == 'all':
                reports = Reports.objects.filter(structure=Structures.objects.get(pk=pk))
            else:
                reports = Reports.objects.filter(service__name=service)

        dates = []
        services = []
        amounts = []
        sums = []
        for r in reports:
            dates.append(r.date)
            services.append(r.service)
            amounts.append(r.amount)
            sums.append(r.sum)
        df = pandas.DataFrame({'Дата': dates,
                               'Услуга': services,
                               'Количество': amounts,
                               'Сумма': sums,
                               })
        df.to_excel(f'services/reports/{Structures.objects.get(pk=pk)}.xlsx', index=False)

        context['date_start'] = date_start
        context['date_finish'] = date_finish

    return render(request, 'services/listReports.html', context)


def myReports(request):
    context = {
        'menu': menu,
        'userMenu': userMenu,
        'title': 'Мои отчеты',
        'services': Services.objects.filter(structure=Structures.objects.get(employee=Users.objects.get(user=request.user))),
        'structure': Structures.objects.filter(employee=Users.objects.get(user=request.user)).first,
        'userRole': str(Users.objects.get(user=request.user).role),
        'reports': Reports.objects.filter(structure=Structures.objects.get(employee=Users.objects.get(user=request.user)))
    }
    return render(request, 'services/listReports.html', context)

def myServices(request):
    context = {
        'menu': menu,
        'userMenu': userMenu,
        'title': 'Мои услуги',
        'userRole': str(Users.objects.get(user=request.user).role),
        'services': Services.objects.filter(structure=Structures.objects.get(employee=Users.objects.get(user=request.user))),
        'structure': Structures.objects.filter(employee=Users.objects.get(user=request.user)).first,
    }
    return render(request, 'services/listReports.html', context)

