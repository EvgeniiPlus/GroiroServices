# Generated by Django 4.2.4 on 2023-11-21 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_alter_orders_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='phone',
            field=models.CharField(max_length=15, verbose_name='Телефон клиента'),
        ),
    ]