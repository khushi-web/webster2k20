from django.urls import path,include
from . import views



urlpatterns = [
    path('',views.userpage,name="user"),
    path('createprofile',views.createprofile,name="createprofile"),
    path('apply',views.apply,name="apply"),
    path('createEvent',views.createEvent,name="createEvent"),
    path('myCreatedEvents',views.myCreatedEvents,name="myCreatedEvents"),
    path('eventDetails/<int:id>',views.eventDetails,name="eventDetails"),
    path('deleteEvent/<int:id>',views.deleteEvent,name="deleteEvent"),

   ]