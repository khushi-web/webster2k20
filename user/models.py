from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#profile model having one to one relation with User model of django auth

class Profile(models.Model):
    student = models.OneToOneField(User,on_delete=models.CASCADE)
    gender = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    phone = models.IntegerField()
    course_name = models.CharField(max_length=255)
    college_name = models.CharField(max_length=255)
    college_address = models.CharField(max_length=255)
    #this field t be set true if user is confirmed by admin as campus ambassdor
    is_ambassdor= models.BooleanField(default=False)
    dob = models.DateField()
    year = models.DateField()
    def __str__(self):
        return str(self.student)

class Events(models.Model):
    hoster=models.ForeignKey(Profile,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    fees = models.IntegerField()
    college = models.CharField(max_length=255)
    dateCreated= models.DateTimeField(auto_now_add=True)
    dateHost = models.DateField()
    def __str__(self):
        return self.name

class EventMembers(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    member = models.ForeignKey(Profile, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.member)