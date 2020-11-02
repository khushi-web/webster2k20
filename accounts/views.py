from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.conf import settings

#admin can see all the pages  but students cannot 

# Create your views here.
@unauthenticated_user
def registerpage(request):
   
        #takes in the form 
    form = CreateUserForm()
        # when submitted it generates a request to create a new user 
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
                # checks if the from is valid and then saves the form and create 
                #creates new user 
            user = form.save()
                #gets the username 
            username = form.cleaned_data.get('username')
                # displays a message on successful registration of user 
            group = Group.objects.get(name='students') # what this does is since now only students will signup so they
            # are automatically pushed into students group
            user.groups.add(group) 
            #send_mail(subject,message,from_email,to_list,fail_silently=True)
            subject='registering'
            message='thankyou for registering . your account has been created successfully'
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email, settings.EMAIL_HOST_USER]
            
            send_mail(subject,message,from_email,to_list,fail_silently=True)

            messages.success(request, 'Account was created for ' + username)
                # immediately redirects to login
            return redirect('login')

    context = {'form' : form }
    # request is brought from register.html
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginpage(request):
    # takes the request from login page
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')
            # authentication for the user taking its password and username
        user = authenticate(request, username=username, password=password)
        
            # when logging in     
        if user is not None:
            login(request, user)
            return redirect('home')
            # to check whether user login credentials are correct and then redirect him

        else:
                # checks incorrect field and asks him to login again 
            messages.info(request, 'Username OR Password is incorrect')

    context = {}
        # urls access from here 
    return render(request, 'accounts/login.html',context)

def logoutuser(request):
    logout(request)
    return redirect('login')

# this is the page where the logged in users are redirected to 
@login_required(login_url='login') # when user is not logged in 
@admin_only #only admin has right to this page. we can also add multiple users like staff etc.
def homepage(request):
    context={}
    return render(request,'accounts/home.html', context)

#directs to the userpage
def userpage(request):
    context={}
    return render(request, 'accounts/user.html', context)

#redirects to the forbidden page
def forbidden(request):
    context={}
    return render(request, 'accounts/forbidden.html', context)

#redirects to the payment page


def index(request):
    context={}
    return render(request,'accounts/index.html',context)