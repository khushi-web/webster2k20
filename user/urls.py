from django.urls import path,include
from . import views



urlpatterns = [
    path('',views.userpage,name="user"),
    path('createprofile',views.createprofile,name="createprofile"),
    path('apply',views.apply,name="apply"),
    path('createEvent',views.createEvent,name="createEvent"),
    path('myCreatedEvents',views.myCreatedEvents,name="myCreatedEvents"),
    path('eventDetails/<int:id>',views.eventDetails,name="eventDetails"),
    path('myeventDetailed/<int:id>',views.myeventDetailed,name="myeventDetailed"),
    path('deleteEvent/<int:id>',views.deleteEvent,name="deleteEvent"),
    path('viewEvents',views.viewEvents,name="viewEvents"),
    path('appliedEvents',views.appliedEvents,name="appliedEvents"),
    path('addMember/<int:id>',views.addMember,name="addMember"),
   ]