from django.contrib import admin
from .models import SubjectList,SubjectNote,User
# Register your models here.

admin.site.register(User)
admin.site.register(SubjectNote)
admin.site.register(SubjectList)
