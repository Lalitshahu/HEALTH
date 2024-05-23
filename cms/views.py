from django.shortcuts import render, redirect
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


@app.route("/")
def rss():
    rss_feed_url = "https://health.economictimes.indiatimes.com/rss/topstories"
    result = get_posts_details(rss_feed_url)

    if result:
        return render_template("rss.html", data=result)
    else:
        return "No RSS feed URL provided."


if __name__ == "__main__":
    app.run(debug=True)


def index(request):
    return render(request, "index.html")


def symptoms(request):
    symptomusers = User.objects.filter(remail=request.session["USER_MAIL"])
    symptomuser = (symptomusers.first())  # Get the first user object or None if no objects found
    sytmaddata = Symptom.objects.all()
    if request.method == "POST":
        sname = request.POST.get("sname")
        semail = request.POST.get("semail")
        sheight = request.POST.get("sheight")
        sweight = request.POST.get("sweight")
        smessage = request.POST.get("sdesc")
        sfile = request.FILES.get("sfile")
        symptomdt = Symptom(userheight=sheight, userweight=sweight, userchat=smessage, userfile=sfile)

        # Update the existing user object if found
        # if symptomuser:
        #     symptomuser.rname = sname
        #     symptomuser.remail = semail
        #     symptomuser.save()
        # else:
        #     # Create a new user object if not found
        #     symptomuser = User(rname=sname, remail=semail)
        #     symptomuser.save()

        symptomdt.save()
        messages.success(request, "Data Successfully Submitted.")
        return redirect("symptoms")

    return render(request, "symptoms.html",{"symptomdata": symptomuser, 'sytmaddata' : sytmaddata})


def about(request):
    return render(request, "about.html")


def news(request):
    rss_feed_url = "https://health.economictimes.indiatimes.com/rss/topstories"
    result = get_posts_details(rss_feed_url)

    if result:
        return render(request, "news.html", {"data": result})
    else:
        return render(request, "news.html", {"data": None})


def disease(request):
    return render(request, "Disease.html")


def logout(request):
    del request.session["IS_LOGIN"]
    messages.success(request, "Log Out Successfully.")
    return redirect("login")

def adminlogout(request):
    del request.session["IS_ADMIN_LOGIN"]
    messages.success(request, "Log Out Successfully.")
    return redirect("loginadmin")


def register(request):
    if request.method == "POST":
        name = request.POST.get("fname")
        mail = request.POST.get("email")
        passw = request.POST.get("password")
        repass = request.POST.get("rpass")
        if passw == repass:
            formdata = User(rname=name, remail=mail, rpass=passw, rrpass=repass)
            formdata.save()
            messages.success(request, "Thank You For Registration. Now Login!")
            return redirect("login")
        else:
            messages.error(request, "Password must be same.")
            return redirect("register")

    return render(request, "register.html")

def login(request):
    if request.method == "POST":
        gmail = request.POST.get("email")
        epassw = request.POST.get("password")
        logindata = User.objects.all().filter(remail=gmail, rpass=epassw).count()
        if logindata > 0:
            request.session["IS_LOGIN"] = True
            request.session["USER_MAIL"] = gmail
            return redirect("index")
        else:
            messages.success(request, "wrong gmail and password")
            return redirect("login")
    return render(request, "login.html")

def eyes(request):
    return render(request, "eyes.html")

def registeradmin(request):
    if request.method == "POST":
        adname = request.POST.get("adname")
        admail = request.POST.get("ademail")
        adpassw = request.POST.get("adpass")
        adrepass = request.POST.get("adrepass")
        if adpassw == adrepass:
            adminrgdata = Admin(adname=adname, ademail=admail, adpass=adpassw, adrepass=adrepass)
            adminrgdata.save()
            messages.success(request, "Thank You For Registration. Now Login!")
            return redirect("loginadmin")
        else:
            messages.error(request, "Password must be same.")
            return redirect("registeradmin")
    return render(request, "registeradmin.html")

def loginadmin(request):
    if request.method == "POST":
        adgmail = request.POST.get("adlgemail")
        adpassw = request.POST.get("adlgpass")
        adminlogindata = Admin.objects.all().filter(ademail=adgmail, adpass=adpassw).count()
        if adminlogindata > 0:
            request.session["IS_ADMIN_LOGIN"] = True
            request.session["ADMIN_MAIL"] = adgmail
            return redirect("admin")
        else:
            messages.success(request, "wrong gmail and password")
            return redirect("loginadmin")
    return render(request, "loginadmin.html")

def admin(request):
    adprofiledata = Admin.objects.get(ademail=request.session["ADMIN_MAIL"])
    return render(request, "admin.html",{'adprofiledata' : adprofiledata})

def diseaseadmin(request):
    adprofiledata = Admin.objects.get(ademail=request.session["ADMIN_MAIL"])
    return render(request, "diseaseadmin.html",{'adprofiledata' : adprofiledata})
    
def symptomsadmin(request):
    if request.method == "POST":
        sytmurl = request.POST.get("sreplyurl")
        sytmuseremail = request.POST.get("suseremail")
        sytmreplydata = Symptom(symptomurl=sytmurl ,symtuseremail=sytmuseremail)
        sytmreplydata.save()
        messages.success(request,'Data Successfully Sent.')
        return redirect("symptomsadmin")
    adprofiledata = Admin.objects.get(ademail=request.session["ADMIN_MAIL"])
    symptomreplyuser = User.objects.all()
    symptomadmin = Symptom.objects.all() 
    userdetail = User.objects.all()
    combine_symptom = zip(symptomadmin,userdetail)
    return render(request, "symptomsadmin.html",{'adprofiledata' : adprofiledata, 'symptomadmin' : combine_symptom, 'symptomreplyuser' : symptomreplyuser})

def diet(request):
    return render(request, "diet.html")

def heart(request):
    return render(request, "heart.html")


def asthma(request):
    return render(request, "asthma.html")


def hair(request):
    return render(request, "hair.html")

def tb(request):
    return render(request, "tb.html")

def diabetes(request):
    return render(request, "diabetes.html")


def cardio(request):
    return render(request, "cardio.html")


def cancer(request):
    return render(request, "cancer.html")


def neuro(request):
    return render(request, "neuro.html")


def gas(request):
    return render(request, "gas.html")


def kidney(request):
    return render(request, "kidney.html")


def liver(request):
    return render(request, "liver.html")


def chronic(request):
    return render(request, "chronic.html")


def skin(request):
    return render(request, "skin.html")


def bronchitis(request):
    return render(request, "bronchitis.html")


def fitness(request):
    return render(request, "fitness.html")


def mental(request):
    return render(request, "mental.html")


def lifemanage(request):
    return render(request, "lifemanage.html")

def myprofile(request):
    profile_user = User.objects.get(remail=request.session["USER_MAIL"])

    if request.method == "POST":
        profile_user = User.objects.get(remail=request.session["USER_MAIL"])
        uname = request.POST.get("uname")
        uemail = request.POST.get("uemail")
        uage = request.POST.get("usage")
        umobile = request.POST.get("usmobile")
        if uname:
            profile_user.rname = uname
        if uemail:
            profile_user.remail = uemail
        if uage:
            profile_user.rage = uage
        if umobile:
            profile_user.rnumber = umobile
        # profiledt = User(rage=uage,rnumber=umobile)
        # profileuser.rname = uname
        # profileuser.remail = uemail
        profile_user.save()
        messages.success(request, "Data Successfully Updated.")
        return redirect("myprofile")

    return render(request, "myprofile.html", {"profiledata": profile_user})


@csrf_exempt
def forgot_pass(request):
    if request.method == "POST":
        fremail = request.POST.get("email")
        if User.objects.all().filter(remail=fremail).count():
            request.session["FORGOT_PASS"] = fremail
        # else:
        #     return redirect('register')
        changepass = redirect("/forgotpass?otp")  # To get user on otp page.
        if request.method == "POST":
            if not request.POST["OTP"]:
                email = request.POST.get("email")
                print(email)
                SendEmail(email, request)
                return redirect("/forgotpass?otp")
            else:
                otp = request.POST.get("OTP")
                if (
                    otp == request.session["otp"]
                ):  # Compares otp got from user and stored in the cookie.
                    return redirect("changepass")
                else:
                    return HttpResponse("<h1>Incorrect OTP.</h1>")  # Msg
    return render(request, "forgotpass.html")


def SendEmail(email, request):
    otp = str(random.randint(1000, 9999))
    email = EmailMessage("OTP", otp, "BRIGHT HEALTH", to=[email])
    email.send()
    request.session["otp"] = otp


def change_pass(request):
    forgptpassdata = User.objects.get(remail=request.session["FORGOT_PASS"])
    if request.method == "POST":
        forgptpassdata = User.objects.get(remail=request.session["FORGOT_PASS"])
        passwd = request.POST.get("passwd")
        repasswd = request.POST.get("repasswd")
        if passwd == repasswd:
            forgptpassdata.rpass = passwd
            forgptpassdata.rrpass = repasswd
            forgptpassdata.save()
            messages.success(request, "Your Password Is Successfully Updated.")
            return redirect("login")
        else:
            messages.error(request, "Password must be same.")
            return redirect("changepass")
    return render(request, "changepass.html")

# def disease(request):
#     keyword_mappings = {
#         "eyes": "https://www.healthline.com/health/eye-health/home-remedies-for-eye-infection",
#         "attack": "https://www.healthline.com/health/home-remedies-for-heart-pain",
#         "asthma": "https://www.healthline.com/health/severe-asthma/natural-remedies",
#         "hair": "https://www.healthline.com/health/regrow-hair-naturally",
#         "diabetes": "https://www.webmd.com/diabetes/natural-remedies-type-2-diabetes",
#         "tuberculosis": "https://www.thehealthsite.com/home-remedies/tuberculosis-here-are-some-home-remedies-to-accelerate-the-healing-process-791608/",
#         "cardio": "https://newsnetwork.mayoclinic.org/discussion/home-remedies-lifestyle-changes-can-help-your-heart-health/",
#         "cancer": "https://www.patientpower.info/navigating-cancer/natural-remedies-cancer",
#         "neurological": "https://www.healthline.com/health/peripheral-neuropathy-natural-treatments",
#         "gas": "https://www.healthline.com/health/immediate-relief-for-trapped-gas-home-remedies-and-prevention-tips",
#         "kidney": "https://www.healthline.com/health/kidney-infection-home-remedies",
#         "liver": "https://www.healthline.com/health/home-remedies-for-fatty-liver",
#         "chronic": "https://www.healthline.com/health/copd/home-remedies",
#         "skin": "https://healthline.com/health/beauty-skin-care/home-remedies-for-glowing-skin",
#         "flu": "https://www.cdc.gov/flu/symptoms/symptoms.htm",
#         "zikavirus": "https://www.ecdc.europa.eu/en/zika-virus-disease",
#     }
#     keyword = request.POST.get('userInput', '').lower().strip()
#     for key, url in keyword_mappings.items():
#         if keyword == key:
#             return redirect(url)
#         else:
#             return render(request, 'Disease.html')
#     return render(request, "Disease.html")