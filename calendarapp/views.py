# Create your views here.
# cal/views.py

from datetime import datetime, date
from django.http import request
from django.shortcuts import render, redirect
from accounts.decorators import unauthenticated_user, allowed_users, admin_only
from user.models import Profile
from controller.models import CollegeAmbassdor
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.generic import TemplateView
from django.utils.safestring import mark_safe
from datetime import timedelta
import calendar
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


from .models import *
from .utils import Calendar
from .forms import EventForm, AddMemberForm

#def index(request):
 #   pro=Profile.objects.get(student=User)
  #  print(pro.college_name)
   # if pro.is_ambassdor==True:
    #    return redirect(calendar)



    #return HttpResponse('hello')
# for inscription register the right group
def inscription(request):
    g = Group.objects.get(name='CollegeAmbassdor')
    user = User()
    "etc"
    user.groups.add(g)
    user.save()
        

    
#To login
def loggedPage(request):
    userGroup = Group.objects.get(user=request.user).name
    if userGroup == 'CollegeAmbassdor':
        # "do some stuff"
        return redirect('calendarapp:calendar')
    elif (userGroup=='admin' or userGroup=='students'):
        # "do some other stuff"    
        return redirect('user')   
    #else userGroup=='students':
     #    return redirect('user') 
@login_required
def index(request):
    if request.user.is_authenticated:
        return render(request, 'calendarapp/calendar.html',{ 'name':request.user.username})
    else:
        return HttpResponse('/login/')         



def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

class CalendarView(LoginRequiredMixin, generic.ListView):
   # permission_required = 'event.view_event'
    login_url = 'login'
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):      
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context
                



@login_required
def create_event(request):   
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        amount = form.cleaned_data['amount']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            amount=amount,
            end_time=end_time
        )
        return HttpResponseRedirect(reverse('calendarapp:calendar'))
    return render(request, 'calendarapp/event.html', {'form': form})

 #class UserAccessMixin(PermissionRequiredMixin):
  #   def dispatch(self, request, *args, **kwargs):
   #      if(not self.request.user.is_authenticated):
    #         return redirect_to_login(self.request.get_full_path(),
     #        self.get_login_url(),self.get_redirect_field_name())
#
 #         if not self.has_permission():
  #            return redirect('/login')  
   #        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)       

class EventEdit( generic.UpdateView):
   # raise_exception=False
    #permission_required = 'event.edit_event'
    #permission_denied_message="You are not an Ambassdor"
    #login_url='/login/'
    #redirect_field_name='login'
    model = Event
    fields = ['title', 'description', 'start_time', 'end_time','amount']
    template_name = 'event.html'

@login_required
def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    context = {
        'event': event,
        'eventmember': eventmember
    }
    return render(request, 'calendarapp/event-details.html', context)


def add_eventmember(request, event_id):
    #if request.user.user.is_ambassdor:
    forms = AddMemberForm()
    if request.method == 'POST':
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            member = EventMember.objects.filter(event=event_id)
            event = Event.objects.get(id=event_id)
            if request.user.is_authenticated:
                user = forms.cleaned_data['user']
                EventMember.objects.create(
                    event=event,
                    user=user
                )
                return redirect('calendarapp:calendar')
            else:
                print('--------------User limit exceed!-----------------')
    context = {
        'form': forms
    }
    return render(request, 'calendarapp/add_member.html', context)

class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = 'event_delete.html'
    success_url = reverse_lazy('calendarapp:calendar')
