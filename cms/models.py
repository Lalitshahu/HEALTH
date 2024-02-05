from django.db import models


class Register(models.Model):
    rname = models.CharField(max_length=200,null=True)
    remail = models.CharField(max_length=200)
    rpass = models.CharField(max_length=200,null=True)
    rrpass = models.CharField(max_length=200,null=True)


class Login(models.Model):
    lmail = models.CharField(max_length=255)   
    lpasswd = models.CharField(max_length=255) 

class Email(models.Model):
    Email = models.CharField(max_length=200) 
  
    def _str_(self): 
        return f"{self.Email}"
    
class Mprofile(models.Model):
    userage = models.IntegerField(null=True)
    usernumber = models.IntegerField(null=True)

class Symptom(models.Model):
    userheight = models.IntegerField(null=True)
    userweight = models.IntegerField(null=True)
    userchat = models.TextField(null=True, blank=True)
    userfile = models.FileField(upload_to='static/pdf', null=True, blank=True)



# Create your models here.
