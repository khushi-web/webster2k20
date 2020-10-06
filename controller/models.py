from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Applicants(models.Model):
    applicant = models.OneToOneField(User,on_delete=models.CASCADE)
    app_email=models.CharField(max_length=255)
    app_clg=models.CharField(max_length=255)
    dateregisteres= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.applicant)
