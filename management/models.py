from django.db import models

from django.utils import timezone

from django.contrib.auth.models import User

import datetime

class Wishlist(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    deadline = models.DateField(null=True)
    applied = models.DateField('date applied',null=True)
    location = models.CharField(max_length=200,blank=True,default='')
    salary = models.IntegerField(null=True)
    post_url = models.URLField(max_length=2000,blank=True,default='')
    status = models.TextField(blank=True,default='')
    offer = models.DateField('offer date',null=True)
    
    def __str__(self):
        return self.company

    
class Applied(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    applied = models.DateField('date applied')
    deadline = models.DateField(null=True)
    location = models.CharField(max_length=200,blank=True,default='')
    salary = models.IntegerField(null=True)
    post_url = models.URLField(max_length=2000,blank=True,default='')
    status = models.TextField(blank=True,default='')
    offer = models.DateField('offer date',null=True)

    def __str__(self):
        return self.company

class Task(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,blank=True,default='')
    text = models.TextField()
    complete = models.BooleanField(default=False)
    date = models.DateField('created date',null=True)

    def __str__(self):
        return self.text
    

