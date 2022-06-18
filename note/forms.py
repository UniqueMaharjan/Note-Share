from django import forms
from django.forms import ModelForm
from .models import SubjectNote, SubjectList, User


class MyUserCreationForm(forms.Form):
    email = forms.EmailField(label="enter your email here")
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    avatar = forms.ImageField(required=False)

    def is_valid(self) -> bool:
        if (password := self.data["password"]) != self.data["confirm_password"]:
            return False
        if len(password) < 6:
            return False
        if len(password) > 20:
            print("length should be not be greater than 8")
            return False

        return super().is_valid()


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
        fields = ["avatar", "email", "bio"]
