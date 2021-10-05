from django.contrib import admin
from .models import SubjectList,SubjectNote
# Register your models here.

admin.site.register(SubjectNote)
admin.site.register(SubjectList)