from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Students(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    student_name=models.CharField(max_length=100)
    student_email=models.EmailField()
    student_course=models.TextField()


class Notice(models.Model):
    title=models.TextField()
    description=models.TextField()

class Roomate(models.Model):
    mobilenumber=models.CharField(max_length=10)
    name=models.TextField()

class Complaints(models.Model):
    room_number=models.CharField(max_length=4)
    complain=models.TextField()
    date = models.DateTimeField(auto_now_add=True)

