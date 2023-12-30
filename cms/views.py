from django.shortcuts import render,redirect
from django.http import HttpResponse
from cms.models import Register,Login
from django.contrib import messages

def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def news(request):
    return render(request,"news.html")

def disease(request):
    return render(request,"disease.html")

def contact(request):
    return render(request,"contact.html")

def logout(request):
    del request.session["heyyy"]
    messages.success(request,"Log Out Successfully.")
    return redirect('login')
    

def register(request):
    if request.method == 'POST':
        name=request.POST.get("fname")
        mail=request.POST.get("email")
        passw=request.POST.get("password")
        repass=request.POST.get("rpass")
        formdata =Register(rname=name,remail=mail,rpass=passw,rrpass=repass)
        formdata.save()
        messages.success(request,"Thank You For Registration. Now Login!")
        return redirect('login')
       
    return render(request,"register.html")

def login(request):
    if request.method == 'POST':
        gmail =request.POST.get("email")
        epassw =request.POST.get("password")
        logindata =Register.objects.all().filter(remail=gmail,rpass=epassw).count()
        if logindata > 0:
            request.session["heyyy"] = True
            return redirect('index')
        else:
            messages.success(request,"wrong gmail and password")
            return redirect('login')

    return render(request,"login.html")

def eyes(request):
    return render(request,"eyes.html")

def heart(request):
    return render(request,"heart.html")

def asthma(request):
    return render(request,"asthma.html")

def hair(request):
    return render(request,"hair.html")

def diet(request):
    return render(request,"diet.html")

def fitness(request):
    return render(request,"fitness.html")

def mental(request):
    return render(request,"mental.html")

def lifemanage(request):
    return render(request,"lifemanage.html")