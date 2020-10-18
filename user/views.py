from django.shortcuts import render,redirect
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from controller.models import Applicants
from django.contrib.auth.models import User
# Create your views here.

#displays user main page if profile created other wise first ask him to create the profile
def userpage(request):
    try:
        profile = Profile.objects.get(student_id=request.user.id)
        context ={'item' : profile}
        return render(request, 'user/home.html', context)
    except Profile.DoesNotExist:                
        context ={}
        messages.error(request,'first complete ur profile')
        return render(request, 'user/createprofile.html', context)

#create profile function 
@login_required
def createprofile(request):
    if request.method == "POST":
        gender = request.POST['gender']
        
        address = request.POST['address']
        phone = request.POST['phone']
        course_name = request.POST['course']
        college = request.POST['college']
        college_add = request.POST['college']
        dob = request.POST['dob']
        year=request.POST['year']
        #if already profile created then details edited
        try:
            profile = Profile.objects.get(student_id=request.user.id)
            profile.gender = gender
            profile.address = address
            profile.course_name = course_name
            profile.phone = phone
            profile.dob = dob
            profile.college_name = college
            profile.college_address = college_add
            profile.year= year
            profile.save()
            return redirect('user')
#otherwise we create one for the user logged in
        except Profile.DoesNotExist:
            Profile.objects.create(
            gender = gender,
            course_name = course_name,
            address = address,
            phone = phone,
            dob = dob,
            year = year,
            college_name = college,
            college_address = college_add,
            student_id=request.user.id
            ).save()
            messages.success(request,'Details saved')
            return redirect('user')
    else:
        
        return render(request,'user/createprofile.html')
#if user clicks on apply then his details will get saved in Applicant model in 
#controller app
def apply(request):
    
    if request.method=="POST":
        profile = Profile.objects.get(student_id=request.user.id)
        try:
            app = Applicants.objects.get(applicant_id=request.user.id)
            messages.error(request,'already applied')
            return redirect('user')

        except Applicants.DoesNotExist:
            Applicants.objects.create(
                app_clg = profile.college_name,
                app_email = request.user.email,
                applicant_id = request.user.id,
            ).save()
            messages.success(request,'applied')
            return redirect('user')
    return render(request,'user/home.html')
        

                
        
        
        
