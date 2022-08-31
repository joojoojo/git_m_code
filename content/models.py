from django.db import models
import datetime

class TimeSet(models.Model):
    user_id = models.IntegerField(default=0)
    timearea_id = models.IntegerField(default=0)
    time_name = models.CharField(max_length=8, default=True)
    time = models.TimeField(default=datetime.time(8, 00), null=False)
    first_checked = models.BooleanField(default=True)
    second_checked = models.BooleanField(default=True)
    third_checked = models.BooleanField(default=True)

class Time_name(models.Model):
    user_id = models.IntegerField(default=0)
    first_medicine_name = models.CharField(max_length=10, default="약1 이름")
    second_medicine_name = models.CharField(max_length=10, default="약2 이름")
    third_medicine_name = models.CharField(max_length=10, default="약3 이름")
