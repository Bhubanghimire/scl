from django import forms
from .models import Parent
from administration.models import User

class ParentForm(forms.ModelForm):

    class Meta:
        model = Parent
        fields = ('name','relationship','contact','email','district','address')

