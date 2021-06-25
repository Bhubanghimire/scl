from django import forms
from .models import Admission, Staff,Routine,ClassRoom, Subject,Notice,User
class StudentAdmission(forms.ModelForm):


    roll_no=forms.CharField(
        widget=forms.TextInput(attrs={'class' : 'myfieldclass'}),
         help_text='Roll No should not match.'
    )
    registration_no=forms.CharField(
         help_text='Reg. should be new.'
    )
    class Meta:
        model = Admission
        fields = ('name', 'dob','phone','gender','current_address','permanent_address','email','image','sesson','class_level','roll_no','registration_no')


class AddStaff(forms.ModelForm):

    class Meta:
        model = Staff
        fields = ('name', 'Type','dob','phone','gender','district','address','email','image')



# from django.core.exceptions import ObjectDoesNotExist


# class AddRoutines(forms.ModelForm):
#     c_lass = forms.CharField(max_length=100)
#     def __init__(self, *args, **kwargs):
#         super(AddRoutines, self).__init__(*args, **kwargs)
#         print(self.instance.Class)
#         try:
#             self.fields['c_lass'].initial = self.instance.Class
#         except ObjectDoesNotExist:
#             self.fields['c_lass'].initial = 'looks like no instance was passed in'

#     def save(self, commit=True):
#         model = super(AddRoutines, self).save(commit=False)
#         saddr = self.cleaned_data['c_lass']
#         print(model,saddr)
#         if saddr:
#             if model.Class:
#                 model.Class = saddr
#                 print(model.Class)
#                 model.address.save()
        

#         if commit:
#             model.save()

#         return model

    # class Meta:
    #     exclude = ('Class',)

class AddRoutines(forms.ModelForm):

    class Meta:
        model = Routine
        fields = ('period','day')


class Newclass(forms.ModelForm):
    class_level=forms.CharField(
        widget=forms.TextInput(attrs={'class' : 'myfieldclass'}),
         help_text='Enter class like: nursary,lkg, class 1, class 2...'
    )
    section=forms.CharField(
        widget=forms.TextInput(attrs={'class' : 'myfieldclass'}),
         help_text='Enter class like:A,B,C..'
    )

    class Meta:
        model = ClassRoom
        fields = ('class_level', 'section','room_number')


class Newsubjects(forms.ModelForm):

    class Meta:
        model = Subject
        fields = ('name','book_ID')


class NewNotice(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ('title', 'postby','detail')


class UserUpdateform(forms.ModelForm):
    class Meta:
        model = User
        fields= ('is_active', 'is_admin','is_teacher','is_student','is_parent','is_principal','is_viceprinciple','is_accountant')     
