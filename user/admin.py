from django.contrib import admin
from .models import Profile,Events,EventMembers
# Register your models here.
admin.site.register(Profile)
admin.site.register(Events)
admin.site.register(EventMembers)