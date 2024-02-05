from django.shortcuts import render,redirect
from django.http import HttpResponse
from cms.models import *
from django.contrib import messages
from django.core.mail import EmailMessage
import random
from django.views.decorators.csrf import csrf_exempt
import feedparser
from flask import Flask, render_template


app = Flask(__name__)
def get_posts_details(rss=None): 
    
    """ 
    Take link of rss feed as argument 
    """
    if rss is not None:
        try:
            # Parsing the blog feed
            blog_feed = feedparser.parse(rss)
            
            # Getting a list of blog entries via .entries
            posts = blog_feed.entries

            # Dictionary for holding posts details
            posts_details = {
                "Title": blog_feed.feed.title,
                "Url": blog_feed.feed.link,
                "Description": blog_feed.feed.description,
                # "Image": blog_feed.feed.image,
                # "PubDate": blog_feed.feed.pubDate
            }

            post_list = []

            # Iterating over individual posts
            for post in posts:
                temp = dict()

                # If any post doesn't have information then throw an error.
                try:
                    temp["Title"] = post.title
                    temp["Link"] = post.link
                    temp["Description"] = post.description
                    # temp["Image"] = post.image
                    # temp["PubDate"] = post.pubDate
                except (AttributeError, KeyError) as e:
                    print(f"Error processing post: {e}")

                post_list.append(temp)

            # Storing lists of posts in the dictionary
            posts_details["posts"] = post_list

            return posts_details  # Returning the details as a dictionary
        except Exception as e:
            print(f"Error parsing RSS feed: {e}")
            return None 
    else:
        return None
    
@app.route('/')
def rss():
    rss_feed_url = "https://health.economictimes.indiatimes.com/rss/topstories"
    result = get_posts_details(rss_feed_url)

    if result:
        return render_template('rss.html', data=result)
    else:
        return "No RSS feed URL provided."

if __name__ == '__main__':
    app.run(debug=True)

    
# def rss(request):
#     rss_feed_url = "https://health.economictimes.indiatimes.com/rss/topstories"
#     result = get_posts_details(rss_feed_url)

#     if result:
#         return render(request, 'rss.html', {'data': result})
#     else:
#         return render(request, 'rss.html', {'data': None})


def index(request):
    return render(request,"index.html")

def symptoms(request):
    symptomuser = Register.objects.get(remail = request.session['USER_MAIL'])
    if request.method == 'POST':
        symptomuser = Register.objects.get(remail = request.session['USER_MAIL'])
        sname = request.POST.get("sname")
        semail = request.POST.get("semail")
        sheight = request.POST.get("sheight")
        sweight = request.POST.get("sweight")
        smessage = request.POST.get("sdesc")
        sfile = request.FILES.get("sfile")
        symptomdt = Symptom(userheight=sheight, userweight=sweight, userchat=smessage, userfile=sfile)
        symptomuser.rname = sname
        symptomuser.remail = semail
        symptomdt.save()
        return redirect('symptoms')  

    return render(request, "symptoms.html",{'symptomdata' : symptomuser})
    
def about(request):
    return render(request,"about.html")

def news(request):
    rss_feed_url = "https://health.economictimes.indiatimes.com/rss/topstories"
    result = get_posts_details(rss_feed_url)

    if result:
        return render(request, 'news.html', {'data': result})
    else:
        return render(request, 'news.html', {'data': None})
    
def disease(request):
    return render(request,"disease.html")


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
        profiledt.save()
        messages.success(request,'Data Successfully Updated.')
        return redirect('myprofile')
        
    return render(request,"myprofile.html",{'profiledata' : profileuser})

@csrf_exempt
def forgot_pass(request):
    if request.method == 'POST':
        fremail = request.POST.get("email")
        if Register.objects.all().filter(remail=fremail).count():
            request.session['FORGOT_PASS'] = fremail
        # else: 
        #     return redirect('register')
        changepass = redirect("/forgotpass?otp")# To get user on otp page.
        if request.method == 'POST':    
            if not request.POST['OTP']:
                email=request.POST.get('email')
                print(email)
                SendEmail(email,request)
                return redirect('/forgotpass?otp')
            else:
                otp = request.POST.get("OTP")
                if otp == request.session["otp"]:# Compares otp got from user and stored in the cookie.
                    return redirect("changepass")
                else:
                    return HttpResponse("<h1>Incorrect OTP.</h1>") #Msg
    return render(request,"forgotpass.html")            

def SendEmail(email,request):
    otp = str(random.randint(1000, 9999))
    email = EmailMessage('OTP', otp ,'BRIGHT HEALTH', to=[email])
    email.send()
    request.session["otp"]=otp

def change_pass(request):
    forgptpassdata = Register.objects.get(remail = request.session['FORGOT_PASS'])
    if request.method == 'POST':
        forgptpassdata = Register.objects.get(remail = request.session['FORGOT_PASS'])
        passwd = request.POST.get("passwd")
        repasswd = request.POST.get("repasswd")
        if passwd == repasswd:    
            forgptpassdata.rpass = passwd
            forgptpassdata.rrpass = repasswd
            forgptpassdata.save()
            messages.success(request,'Your Password Is Successfully Updated.')
            return redirect("login")
        else:
            messages.error(request,"Password must be same.")
            return redirect('changepass')        
    return render(request,"changepass.html") 

 