from django.contrib import admin

from cms.models import *

class Registerhead(admin.ModelAdmin):
    list_display=('rname','remail','rpass','rrpass')

admin.site.register(Register,Registerhead)


class Loginhead(admin.ModelAdmin):
    list_display=('lmail','lpasswd')

admin.site.register(Login,Loginhead)


class Mprofilehead(admin.ModelAdmin):
    list_display=('userage','usernumber')

admin.site.register(Mprofile,Mprofilehead)

class Symptomshead(admin.ModelAdmin):
    
    list_display=('userheight','userweight','userchat','userfile')

admin.site.register(Symptom,Symptomshead) 

admin.site.register(Email)
# Register your models here.