from django.http import HttpResponse
from django.shortcuts import redirect
from . import views 
# a decorator is a function that takes in the original function and adds in extra 
#functionality which is called before the main function

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:# if user is authenticated 
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs) # otherwise calling
            #this function will execute all steps from the views.py file 

    return wrapper_func

def allowed_users(allowed_roles=[]): # only specific entries (see views)
    def decorator(view_func): # view_func is expanded and worked upon here (gives permission factors for the two types of user)
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists(): #if the classified groups exists so as to differentiate 
                group = request.user.groups.all()[0].name # name of 1st grp in the list

            if group in allowed_roles: # user is in allowed group
                return view_func(request, *args, **kwargs)
            else: # does not exist in that group (restrict)
                return redirect('forbidden')
        return wrapper_func
    return decorator 
 # what exactly happens in the above call is that first the decorator in called so as to provide specifications to
 # which in turn calls view_func related to the login page during time of registering/login . wrapper function
 # then continues the process of logging in and registering . the permissions for college students and admin is based on 
 # 'superuser status' and 'staff status' default attributes which is true for admin('see django admin it is ticked') and not for users
 # which is main factor that distinguishes them.
 #but here in order to avoid messiness we use default django 'GROUPS' (see admin panel). and we will add permission checks 
 # to classify admin into admin group and other users into college group 

 # the allowed_users are checked and directed into their specific panels . see their working in views


#set work for admin and user

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        if group == 'students': # there are two groups made in admin panel 1.admin: for admin only 2.students : college ones
            return redirect('user')

        if group == 'admin':
            return view_func(request, *args, **kwargs)
   

    return wrapper_function

        