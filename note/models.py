from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(unique=True,null=True)
    bio = models.TextField(null=True,blank=True)
    avatar = models.ImageField(default = "images/avatar.svg",upload_to = "images",null = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email

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
    # @property
    # def file_name(self):
    #     file = self.file_upload.find('/')
    #     filename = self.file_upload[file+1:]
    #     return filename

