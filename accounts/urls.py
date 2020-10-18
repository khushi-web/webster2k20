from django.urls import path,include
from django.conf.urls import url
from . import views


''' from here redirecting to individual app
as per the logged in is admin or user '''
urlpatterns = [
    path('login/',views.loginpage,name="login"),
    path('register/',views.registerpage,name="register"),
    
    path('logout/', views.logoutuser, name="logout"),
    path('user/', include('user.urls')),
    path('calendarapp/',include('calendarapp.urls')),
    path('controller/', include('controller.urls')),
    path('forbidden/', views.forbidden, name="forbidden"),
]