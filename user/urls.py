from django.urls import path,include
from . import views



urlpatterns = [
    path('',views.userpage,name="user"),
    path('createprofile',views.createprofile,name="createprofile"),
    path('apply',views.apply,name="apply"),
   ]