from django.contrib import admin
from .models import SubjectList,SubjectNote, UserProfile
# Register your models here.

admin.site.register(SubjectNote)
admin.site.register(SubjectList)
admin.site.register(UserProfile)