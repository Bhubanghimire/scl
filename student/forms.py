from django import forms
from .models import Parent

class ParentForggm(forms.ModelForm):

    class Meta:
        model = Parent
        fields = ('father_name', 'mother_name','occupation','contact','email','district','address','image')
