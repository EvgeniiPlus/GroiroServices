# Generated by Django 4.2.4 on 2023-11-09 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_alter_reports_nds'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reports',
            name='nds',
            field=models.FloatField(blank=True, default=0, verbose_name='Из них НДС'),
        ),
    ]