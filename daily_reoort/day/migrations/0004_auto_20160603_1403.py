# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-03 05:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('day', '0003_book_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='page',
            field=models.IntegerField(blank=True, default=0, verbose_name='ページ'),
        ),
    ]
