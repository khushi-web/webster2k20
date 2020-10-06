from django.shortcuts import render
from accounts.decorators import unauthenticated_user, allowed_users, admin_only
from user.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Applicants
# Create your views here.
@login_required(login_url='login') # when user is not logged in 
@admin_only #only admin has right to this page. we can also add multiple users like staff etc.
def homepage(request):
    context={}
    return render(request,'controller/home.html', context)

def viewapplicants(request):
    item = Applicants.objects.all()
    context ={'item' : item}
    return render(request,'controller/viewapp.html',context)