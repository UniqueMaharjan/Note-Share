from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
# Create your models here.
class SubjectList(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class SubjectNote(models.Model):
    host= models.ForeignKey(User, on_delete= models.SET_NULL,null=True)
    topic = models.ForeignKey(SubjectList, on_delete= models.CASCADE)
    name = models.CharField(max_length=200)
    body = models.TextField(null = True,blank=True)
    file_upload = models.FileField(upload_to = "files",null=True,blank=True)
    created = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated','-created']
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    profile_pic = models.ImageField(upload_to = "profile")

    def __str__(self):
        return f'Profile of {self.user}'