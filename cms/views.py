from django.shortcuts import render,redirect
from django.http import HttpResponse
from cms.models import *
from django.contrib import messages
from django.core.mail import EmailMessage
import random
from django.views.decorators.csrf import csrf_exempt

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
    del request.session["IS_LOGIN"]
    messages.success(request,"Log Out Successfully.")
    return redirect('login')
    

def register(request):
    if request.method == 'POST':
        name=request.POST.get("fname")
        mail=request.POST.get("email")
        passw=request.POST.get("password")
        repass=request.POST.get("rpass")
        if passw == repass:
            formdata =Register(rname=name,remail=mail,rpass=passw,rrpass=repass)
            formdata.save()
            messages.success(request,"Thank You For Registration. Now Login!")
            return redirect('login')
        else:
            messages.error(request,"Password must be same.")
            return redirect('register')
       
    return render(request,"register.html")

def login(request):
    if request.method == 'POST':
        gmail =request.POST.get("email")
        epassw =request.POST.get("password")
        logindata =Register.objects.all().filter(remail=gmail,rpass=epassw).count()
        if logindata > 0:
            request.session["IS_LOGIN"] = True
            request.session['USER_MAIL'] = gmail
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

def myprofile(request):
    profileuser = Register.objects.get(remail = request.session['USER_MAIL'])
    if request.method == 'POST':
        profileuser = Register.objects.get(remail = request.session['USER_MAIL'])
        uname = request.POST.get("uname")
        uemail = request.POST.get("uemail")
        uage=request.POST.get("usage")
        umobile=request.POST.get("usmobile")
        profiledt = Mprofile(userage=uage,usernumber=umobile)
        profileuser.rname = uname
        profileuser.remail = uemail
        # profileuser.save()
        profiledt.save()
        messages.success(request,'Data Successfully Updated.')
        return redirect('myprofile')
    
    return render(request,"myprofile.html",{'profiledata' : profileuser})

@csrf_exempt
def forgot_pass(request):
    changepass=redirect("/forgotpass?otp")# To get user on otp page.
    if request.method == 'POST':    
        if not request.POST['OTP']:
            email=request.POST.get('email')
            print(email)
            SendEmail(email,request)
            return redirect('/forgotpass?otp')
        else:
            otp = request.POST.get("OTP")
            if otp == request.session["otp"]:#Compares otp got from user and stored in the cookie.
                return redirect("changepass")
            else:
                return HttpResponse("<h1>Incorrect OTP.</h1>") #Msg
    return render(request,"forgotpass.html")            

def SendEmail(email,request):
    otp = str(random.randint(1000, 9999))
    email = EmailMessage('OTP', otp ,to=[email])
    email.send()
    request.session["otp"]=otp

def change_pass(request):
    return render(request,"changepass.html") 

 