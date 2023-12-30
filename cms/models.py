from django.db import models


class Register(models.Model):
    rname= models.CharField(max_length=200,null=True)
    remail= models.CharField(max_length=200)
    rpass= models.CharField(max_length=200,null=True)
    rrpass= models.CharField(max_length=200,null=True)


class Login(models.Model):
    lmail=models.CharField(max_length=255)   
    lpasswd=models.CharField(max_length=255) 
# Create your models here.
