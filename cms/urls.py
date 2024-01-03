from django.urls import path
from cms import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('news/',views.news,name='news'),
    path('disease/',views.disease,name='disease'),
    path('login/',views.login,name='login'),
    path('eyes/',views.eyes,name='eyes'),
    path('register/',views.register,name='register'),
    path('heart/',views.heart,name='heart'),
    path('asthma/',views.asthma,name='asthma'),
    path('diet/',views.diet,name='diet'),
    path('fitness/',views.fitness,name='fitness'),
    path('mental/',views.mental,name='mental'),
    path('lifemanage/',views.lifemanage,name='lifemanage'),
    path('hair/',views.hair,name='hair'),
    path('logout',views.logout,name="logout"),
    path('myprofile',views.myprofile,name="myprofile"),
    path('forgotpass',views.forgot_pass,name="forgotpass"),
    path('changepass',views.change_pass,name="changepass"),
]