from django.shortcuts import render,redirect
from .models import Profile
from .models import ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile,Events,EventMembers
from controller.models import Applicants
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, get_connection
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
        profile = Profile.objects.get(student_id=request.user.id)
        context ={'item' : profile}
        return render(request,'user/createprofile.html',context)
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
    profile = Profile.objects.get(student_id=request.user.id)
    context ={'item' : profile}
    return render(request,'user/home.html',context)

#to create a event 
#only ambassdor is shown this option
#thou we also have  a check for some smart userss
def createEvent(request):
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        dateHosting = request.POST['dateHosting']
        fees = request.POST['fees']


        try:
            profile = Profile.objects.get(student_id=request.user.id)
            if profile.is_ambassdor == True:
                Events.objects.create(
                    name=name,
                    description=description,
                    fees = fees,
                    dateHost = dateHosting,
                    hoster_id=profile.id,
                    college = profile.college_name
                ).save()

                messages.success(request, 'Event successfully Created')
                return redirect('user')
            else:
                messages.warning(request, 'NOT A CAMPUS AMBASSDOR')
                return redirect('user')


        except Profile.DoesNotExist:
            messages.warning(request, 'You Must Complete Your Profile Before Creating An event')
            return render(request, 'user/home.html')

    else:
        profile = Profile.objects.get(student_id=request.user.id)
        context ={'item' : profile}
        return render(request, 'user/createEvent.html',context)

        
#for campus ambassdor to view events he has created
def myCreatedEvents(request):

    try:
        profile = Profile.objects.get(student_id=request.user.id)
        events = Events.objects.filter(hoster_id = profile.id)
        context = {'events': events,'item' : profile}
        
    except:
        events = []
        context = {'events': events,'item' : profile}
        

    return render(request,'user/ViewEvents.html',context)


#this function is used to return details of a particular event
#used when ambassdor views the detailed view of his created event 
#and secondly when a non ambassdor views the details of event of his colleges(note : not of his applied events)
def eventDetails(request,id):
    profile = Profile.objects.get(student_id=request.user.id)
    event = Events.objects.get(pk=id)
    context = {'event': event,'item' : profile}
    return render(request,'user/EventDetails.html',context)

#to delete a event only hoster has the right to delete ;else noone can
def deleteEvent(request,id):
    profile = Profile.objects.get(student_id=request.user.id)
    item=Events.objects.get(pk=id)
    if item.hoster_id ==profile.id:
        item.delete()
        messages.warning(request,'Event has been deleted')
        return redirect('myCreatedEvents')  
    else:
        messages.warning(request,'u r not authorized to delete it')
        return redirect('user') 

# this function is for non-ambassdors
#to view the events created for his college
def viewEvents(request):
    try:
        profile = Profile.objects.get(student_id=request.user.id)
        print(profile.college_name)
        events = Events.objects.filter(college = profile.college_name)
        context = {'events': events,'item' : profile}
        
    except:
        events = []
        
        context = {'events': events,'item' : profile}
    return render(request,'user/Viewevents.html',context)

#when a non-ambassdor requests to be a part of the corr event
def addMember(request,id):
    item= Events.objects.get(pk=id)
    profile = Profile.objects.get(student_id=request.user.id)
    
    try:
        members = EventMembers.objects.get(event_id=item.id,member_id=profile.id)
        print(members)
        messages.warning(request,'already added')
        return redirect('user') 
    except:
        EventMembers.objects.create(
            event_id=item.id,
            member_id=profile.id
        ).save()
        messages.success(request,'added to your list')
        return redirect('user') 

#for a non-ambassdor to view the list of events where he has applied
def appliedEvents(request):
    try:
        profile = Profile.objects.get(student_id=request.user.id)
        members = EventMembers.objects.filter(member_id=profile.id) 
        events=[]
        for i in members:
            a = Events.objects.get(id = i.event_id)
            events.append(a)
            print(events)
        context = {'events': events,'item' : profile}
    except:
        events = []
        
        context = {'events': events,'item' : profile}
    return render(request,'user/AppliedEvents.html',context)

#when a non-ambassdor wants to see the event in detail to which he has applied
#clock to be added here
def myeventDetailed(request,id):
    profile = Profile.objects.get(student_id=request.user.id)
    event = Events.objects.get(pk=id)
    context = {'event': event,'item' : profile}
    return render(request,'user/MyeventDetailed.html',context)

def contact(request):
        submitted = False
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                # assert False
                con = get_connection('django.core.mail.backends.console.EmailBackend')
                send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@example.com'),
                ['cairocoders0711@gmail.com'],
                connection=con
             )
            return HttpResponseRedirect('/contact?submitted=True')
        else:
            form = ContactForm()
            if 'submitted' in request.GET:
                submitted = True
                return render(request, 'contact/contact.html', {'form': form, 'submitted': submitted})