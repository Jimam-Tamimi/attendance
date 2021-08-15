from time import time
from django.db.models.deletion import CASCADE
from django.db import models
from home.models import MyUser
import random
import string
from django.utils import timezone
from django.conf import settings
def generate_key():
    return ''.join(random.choice(string.ascii_letters + string.digits  + "_-") for _ in range(settings.TOKEN_LENGTH))
def generate_code():
    return int(''.join(random.choice(string.digits ) for _ in range(settings.CODE_LENGTH)))

# Create your models here.
class Student(models.Model):
    student = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.student)


class Class(models.Model):
    name = models.CharField("Class Name", max_length=100, blank=False)
    time = models.TimeField("Class Time", blank=False)
    students = models.ManyToManyField(Student, blank=True, verbose_name="Students In This Class")
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.name)




class Link(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="Class")
    token = models.CharField("Key", max_length=1024,  unique=True, blank=True)
    code = models.IntegerField("Code", unique=True, blank=True)
    timestamp = models.DateTimeField("Link Creation Time", auto_now_add=True)
    expiry = models.DateTimeField("Expiry Date Time", blank=False, null=False)

    def save(self,*args, **kwargs):
        token = ''
        while True:
            token = generate_key()
            if(len(Link.objects.filter(token=token)) != 0):
                continue
            else:
                break
        self.token = token
        code = 0
        while True:
            code = generate_code()
            if(len(Link.objects.filter(code=code)) != 0):
                continue
            else:
                break
        self.code = code
        super(Link, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.class_name)


class Attendance(models.Model):
    student = models.ForeignKey(Student, verbose_name="Students", blank=False, on_delete=models.CASCADE)
    # attendance_date = models.DateField("Attendance Date")
    # attendance_time = models.TimeField("Attendance Time")
    attendance_date = models.DateField("Attendance Date", auto_now_add=True)
    attendance_time = models.TimeField("Attendance Time", auto_now_add=True)
    link = models.ForeignKey(Link, on_delete=models.CASCADE, blank=False, null=False)


    def __str__(self):
        return str(self.student)

