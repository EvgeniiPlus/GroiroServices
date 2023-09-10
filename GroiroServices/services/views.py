import mimetypes
import os
from datetime import datetime, tzinfo, timezone
from wsgiref.util import FileWrapper
from pytils import translit
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import *
from django.http import HttpResponse, HttpResponseNotFound, StreamingHttpResponse, FileResponse
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
        'services': Services.objects.filter(
            structure=Structures.objects.get(employee=Users.objects.get(user=request.user))),
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
            sum = round(int(service_count_list[i]) * Services.objects.filter(pk=service_id_list[i])[0].price, 2)
            if int(service_count_list[i]) != 0:
                Reports.objects.create(
                    date=date,
                    service=Services.objects.get(pk=service_id_list[i]),
                    structure=Structures.objects.filter(employee=Users.objects.get(user=request.user))[0],
                    amount=service_count_list[i],
                    sum=sum,
                    nds=round(sum * 0.2, 2)
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
        'structure': Structures.objects.filter(pk=pk).first,
        'services': Services.objects.filter(structure=Structures.objects.get(pk=pk)),
        'userRole': str(Users.objects.get(user=request.user).role),
        'reports': Reports.objects.filter(structure=pk).order_by('-date')
    }

    if request.method == 'POST':
        date_start = str(request.POST.get('date_start'))
        date_finish = str(request.POST.get('date_finish'))

        if date_start and date_finish != '':
            reports = Reports.objects.filter(structure=Structures.objects.get(pk=pk),
                                             date__gte=date_start,
                                             date__lte=date_finish)

        else:
            reports = Reports.objects.filter(structure=Structures.objects.get(pk=pk))

        dates = []
        services = []
        amounts = []
        sums = []

        for r in reports:
            dates.append(r.date)
            services.append(r.service)
            amounts.append(r.amount)
            sums.append(r.sum)

        dates.append('')
        sums.append(f'=SUM(D2:D{len(sums) + 1})')
        amounts.append(f'=SUM(C2:C{len(amounts) + 1})')
        services.append('Итого:')

        df = pandas.DataFrame({'Дата': dates,
                               'Услуга': services,
                               'Количество': amounts,
                               'Сумма': sums,
                               })
        if date_start and date_finish == '':
            filename = f'{translit.slugify(Structures.objects.get(pk=pk).name)}_all_time'
        else:
            filename = f'{translit.slugify(Structures.objects.get(pk=pk).name)}_{date_start}-{date_finish}'

        filepath = f'services/reports/{filename}.xlsx'
        df.to_excel(filepath, index=False)

        chunk_size = 8192

        response = StreamingHttpResponse(FileResponse(open(filepath, 'rb'), chunk_size),
                                         content_type=mimetypes.guess_type(filepath)[0])

        response['Content-Length'] = os.path.getsize(filepath)
        response['Content-Disposition'] = "attachment; filename=%s" % filename

        context['date_start'] = date_start
        context['date_finish'] = date_finish

        return response

    return render(request, 'services/listReports.html', context)


def myReports(request):
    context = {
        'menu': menu,
        'userMenu': userMenu,
        'title': 'Мои отчеты',
        'services': Services.objects.filter(
            structure=Structures.objects.get(employee=Users.objects.get(user=request.user))),
        'structure': Structures.objects.filter(employee=Users.objects.get(user=request.user)).first,
        'userRole': str(Users.objects.get(user=request.user).role),
        'reports': Reports.objects.filter(
            structure=Structures.objects.get(employee=Users.objects.get(user=request.user)))
    }

    if request.method == 'POST':
        date_start = str(request.POST.get('date_start'))
        date_finish = str(request.POST.get('date_finish'))
        structure = Structures.objects.filter(employee=Users.objects.get(user=request.user))[0]

        if date_start and date_finish != '':
            reports = Reports.objects.filter(structure=structure,
                                             date__gte=date_start,
                                             date__lte=date_finish)

        else:
            reports = Reports.objects.filter(structure=structure)

        dates = []
        services = []
        amounts = []
        sums = []

        for r in reports:
            dates.append(r.date)
            services.append(r.service)
            amounts.append(r.amount)
            sums.append(r.sum)

        dates.append('')
        sums.append(f'=SUM(D2:D{len(sums) + 1})')
        amounts.append(f'=SUM(C2:C{len(amounts) + 1})')
        services.append('Итого:')
        print(amounts)
        df = pandas.DataFrame({'Дата': dates,
                               'Услуга': services,
                               'Количество': amounts,
                               'Сумма': sums,
                               })
        if date_start and date_finish == '':
            filename = f'{translit.slugify(structure)}_all_time'
        else:
            filename = f'{translit.slugify(structure)}_{date_start}-{date_finish}'

        filepath = f'services/reports/{filename}.xlsx'
        df.to_excel(filepath, index=False)

        chunk_size = 8192

        response = StreamingHttpResponse(FileResponse(open(filepath, 'rb'), chunk_size),
                                         content_type=mimetypes.guess_type(filepath)[0])

        response['Content-Length'] = os.path.getsize(filepath)
        response['Content-Disposition'] = "attachment; filename=%s" % filename

        context['date_start'] = date_start
        context['date_finish'] = date_finish

        return response

    return render(request, 'services/listReports.html', context)


def myServices(request):
    context = {
        'menu': menu,
        'userMenu': userMenu,
        'title': 'Мои услуги',
        'userRole': str(Users.objects.get(user=request.user).role),
        'services': Services.objects.filter(
            structure=Structures.objects.get(employee=Users.objects.get(user=request.user))),
        # 'structure': Structures.objects.filter(employee=Users.objects.get(user=request.user)).first,
    }

    if request.method == 'POST':
        pks = request.POST.getlist('pk')
        names = request.POST.getlist('name')
        descriptions = request.POST.getlist('description')
        prices = request.POST.getlist('price')

        # Services.objects.bulk_update(
        #     [names[i]] for i in range(len(names)),
        #
        # )
        for i in range(len(names)):
            Services.objects.filter(pk=pks[i]).update(name=names[i], description=descriptions[i], price=prices[i])

        return redirect('myServices')

    return render(request, 'services/myServices.html', context)


def del_service(request, pk):
    Services.objects.get(pk=pk).delete()
    return redirect(myServices)


def newService(request):
    context = {
        'menu': menu,
        'userMenu': userMenu,
        'title': 'Новая услуга',
        'userRole': str(Users.objects.get(user=request.user).role),
        'structure': Structures.objects.filter(employee=Users.objects.get(user=request.user)).first,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')

        Services.objects.create(name=name, description=description, price=price,
                                structure=Structures.objects.filter(employee=Users.objects.get(user=request.user))[0])
        return redirect('myServices')

    return render(request, 'services/newService.html', context)
