from django.contrib import admin

from cms.models import Register,Login

class Registerhead(admin.ModelAdmin):
    list_display=('rname','remail','rpass','rrpass')

admin.site.register(Register,Registerhead)


class Loginhead(admin.ModelAdmin):
    list_display=('lmail','lpasswd')

admin.site.register(Login,Loginhead)
# Register your models here.