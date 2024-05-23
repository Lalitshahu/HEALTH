from django.db import models


class User(models.Model):
    rname = models.CharField(max_length=200,null=True)
    remail = models.CharField(max_length=200,null=True) 
    rpass = models.CharField(max_length=200,null=True)
    rrpass = models.CharField(max_length=200,null=True)
    rage = models.IntegerField(null=True)
    rnumber = models.IntegerField(null=True)

class Email(models.Model):
    Email = models.CharField(max_length=200) 
  
    def _str_(self): 
        return f"{self.Email}"
    
# class Mprofile(models.Model):
#     userage = models.IntegerField(null=True)
#     usernumber = models.IntegerField(null=True)

class Symptom(models.Model):
    userheight = models.IntegerField(null=True)
    userweight = models.IntegerField(null=True)
    userchat = models.TextField(null=True, blank=True)
    userfile = models.FileField(upload_to='static/pdf', null=True, blank=True)
    symptomurl = models.TextField(null=True, blank=True)
    symtuseremail = models.CharField(max_length=200,null=True)

class Admin(models.Model):
    adname = models.CharField(max_length=200,null=True)
    ademail = models.CharField(max_length=200,null=True)
    adpass = models.CharField(max_length=200,null=True)
    adrepass = models.CharField(max_length=200,null=True)

# Create your models here.
