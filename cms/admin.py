from django.contrib import admin

from cms.models import *

class userhead(admin.ModelAdmin):
    list_display=('rname','remail','rpass','rrpass','rage','rnumber')

admin.site.register(User,userhead)


class Symptomshead(admin.ModelAdmin):
    
    list_display=('userheight','userweight','userchat','userfile', 'symptomurl', 'symtuseremail')

admin.site.register(Symptom,Symptomshead) 

class Adminhead(admin.ModelAdmin):

    list_display=('adname', 'ademail', 'adpass', 'adrepass')

admin.site.register(Admin,Adminhead)

admin.site.register(Email)
# Register your models here.