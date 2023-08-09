from django.contrib.auth.models import User
from django.db import models



class Users(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    name = models.CharField(max_length=150, verbose_name="Имя, отчество")
    role = models.ForeignKey('Roles', on_delete=models.PROTECT, verbose_name='Роль')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.surname} {self.name}'


class Roles(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.name


class Structures(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    employee = models.ForeignKey('Users', on_delete=models.PROTECT, verbose_name="Сотрудник")

    class Meta:
        verbose_name = 'Структура'
        verbose_name_plural = 'Структуры'

    def __str__(self):
        return self.name


class Services(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    structure = models.ForeignKey('Structures', on_delete=models.PROTECT, verbose_name="Структура")
    price = models.FloatField(verbose_name="Стоимость")

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name


class Reports(models.Model):
    date = models.DateField(verbose_name='Дата')
    service = models.ForeignKey('Services', on_delete=models.PROTECT, verbose_name="Услуга")
    amount = models.PositiveIntegerField(verbose_name="Количество")
    sum = models.FloatField(verbose_name="Сумма")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    date_edit = models.DateTimeField(auto_now=True, verbose_name="Изменено")

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'

    def __str__(self):
        return f'{self.date} {self.service}'

