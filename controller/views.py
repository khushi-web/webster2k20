from django.shortcuts import render,redirect
from accounts.decorators import unauthenticated_user, allowed_users, admin_only
from user.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Applicants,CollegeAmbassdor
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

def completedetails(request,id):
    
    item=Applicants.objects.get(pk=id)
    context = {'viewjob':item}
    return render(request,'controller/completedetails.html',context)

def deletejob(request,id):
    
    item=Applicants.objects.get(pk=id)
    item.delete()
    messages.warning(request,'Application has been deleted')
    return redirect('viewapplicants')
    

def confirmApplication(request,id):
    
    item=Applicants.objects.get(pk=id)
    college=item.app_clg
    ambassdor=item.applicant_id

    if not CollegeAmbassdor.objects.filter(college=college).exists():
        CollegeAmbassdor.objects.create(
            college = college,
            ambassdor_id= ambassdor,
            

        ).save()
        pro=Profile.objects.get(student=ambassdor)
        print(pro.college_name)
        pro.is_ambassdor=True
        pro.save()
        messages.success(request,'Application for user '+pro.student.email +' confirmed')
        print(pro.student.email)
        it=Applicants.objects.get(pk=id)
        it.delete()
        item = Applicants.objects.all()
        context ={'item' : item}
        return redirect('viewapplicants')

    else:
        messages.error(request,'Campus ambassdor for college '+college+' already exist')
        item = Applicants.objects.all()
        context ={'item' : item}
        return redirect('viewapplicants')
    