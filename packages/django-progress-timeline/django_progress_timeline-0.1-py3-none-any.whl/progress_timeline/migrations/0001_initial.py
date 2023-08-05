# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-02-20 21:08
from __future__ import unicode_literals

import colorfield.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='date')),
                ('ammount', models.IntegerField(verbose_name='new value')),
            ],
            options={
                'verbose_name': 'current state',
                'verbose_name_plural': 'current states',
            },
        ),
        migrations.CreateModel(
            name='ProgressTimeLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
                ('goal', models.IntegerField(verbose_name='goal')),
                ('start_date', models.DateTimeField(verbose_name='start date')),
                ('end_date', models.DateTimeField(verbose_name='end date')),
                ('date_layout', models.PositiveIntegerField(choices=[(0, 'show all'), (1, 'only start and end date'), (2, 'do not display')], default=0, verbose_name='display date format')),
                ('number_layout', models.PositiveIntegerField(choices=[(0, 'percent'), (1, 'numbers'), (2, 'do not display')], default=0, verbose_name='number layout format')),
                ('background_color', colorfield.fields.ColorField(default=b'#F8F8FF', max_length=18, verbose_name='background color')),
                ('basic_color', colorfield.fields.ColorField(default=b'#ddd', max_length=18, verbose_name='basic color')),
                ('diff_color', colorfield.fields.ColorField(default=b'#B22222', max_length=18, verbose_name='differency color')),
                ('progress_color', colorfield.fields.ColorField(default=b'#228B22', max_length=18, verbose_name='progress color')),
            ],
            options={
                'verbose_name': 'Chart of achievements',
                'verbose_name_plural': 'achievement charts',
            },
        ),
        migrations.AddField(
            model_name='currentprogress',
            name='progress_timeline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='progress_timeline.ProgressTimeLine'),
        ),
    ]
