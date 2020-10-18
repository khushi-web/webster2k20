from django.urls import path,include
from . import views



urlpatterns = [
    path('',views.homepage,name="home"),
    path('viewapplicants',views.viewapplicants,name="viewapplicants"),
    path('completedetails/<int:id>',views.completedetails,name="completedetails"),
    path('confirmApplication/<int:id>',views.confirmApplication,name="confirmApplication"),
    path('deletejob/<int:id>',views.deletejob,name="deletejob"),

]