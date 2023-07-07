from django.shortcuts import render

from .models import *
from django.http import HttpResponse, HttpResponseNotFound, StreamingHttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, CreateView
# Create your views here.
menu = [{'title': 'Главная', 'url_name': 'home'},
        {'title': 'Создать отчет', 'url_name': 'dailyReport'},
]

def home(request):
        context = {
                'menu': menu,
                'title': 'ГрОИРО. Услуги',
        }
        return render(request, 'services/index.html', context)

def dailyReport(request):
        pass