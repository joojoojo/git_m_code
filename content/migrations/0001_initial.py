# Generated by Django 4.0.4 on 2022-05-31 00:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Time_name',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0)),
                ('first_medicine_name', models.CharField(default='약1 이름', max_length=10)),
                ('second_medicine_name', models.CharField(default='약2 이름', max_length=10)),
                ('third_medicine_name', models.CharField(default='약3 이름', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TimeSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0)),
                ('timearea_id', models.IntegerField(default=0)),
                ('time_name', models.CharField(default=True, max_length=8)),
                ('time', models.TimeField(default=datetime.time(8, 0))),
                ('first_checked', models.BooleanField(default=True)),
                ('second_checked', models.BooleanField(default=True)),
                ('third_checked', models.BooleanField(default=True)),
            ],
        ),
    ]
