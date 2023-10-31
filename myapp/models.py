from django.db import models

# Create your models here.
# class

class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    mobile=models.CharField(max_length=10)
    remarks=models.CharField(max_length=200)

class User(models.Model):
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    mobile=models.CharField(max_length=10)
    address=models.CharField(max_length=200)
    password=models.CharField(max_length=40)
    profile_pic=models.ImageField('profile_pic/',default="")