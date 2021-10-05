from django.forms import ModelForm, fields
from .models import SubjectNote,SubjectList

class noteForm(ModelForm):
    class Meta:
        model = SubjectNote
        fields = "__all__"

class listForm(ModelForm):
    class Meta:
        model = SubjectList
        fields = "__all__"