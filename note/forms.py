from django.forms import ModelForm
from .models import SubjectNote,SubjectList,User
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1','password2']

class noteForm(ModelForm):
    class Meta:
        model = SubjectNote
        fields = "__all__"

class listForm(ModelForm):
    class Meta:
        model = SubjectList
        fields = "__all__"

class MyUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name','username','email','bio']