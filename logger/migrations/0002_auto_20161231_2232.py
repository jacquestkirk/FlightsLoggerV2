# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-01 04:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight_info',
            name='query_dateTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='flight_info',
            name='type',
            field=models.CharField(choices=[('CHEAP', 'Cheapest Flight'), ('NOLAY', 'No Layover'), ('TEST', 'For Testing')], max_length=5),
        ),
    ]