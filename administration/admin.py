from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import Admission,ClassRoom,Subject,Contact,Notice,Staff,Routine,User,Registration,Session,Staff_Leave_Application
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

# Register your models here.
admin.site.register(Admission)
admin.site.register(ClassRoom)
admin.site.register(Subject)
admin.site.register(Contact)
admin.site.register(Notice)
admin.site.register(Staff)
admin.site.register(Routine)
admin.site.register(Session)
admin.site.register(Staff_Leave_Application)


# print(UserChangeForm.Meta.fields)
# class MyUserChangeForm(UserChangeForm):

#     class Meta(UserChangeForm.Meta):
#         model = User
#         fields = ('username', 'email')

# class MyUserCreationForm(UserCreationForm):
#     error_message = UserCreationForm.error_messages.update({
#         'duplicate_username':"This Username has already been taken!"
#     })

#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ('username', 'email')

#     def clean_username(self):
#         username = self.cleaned_data['username']
#         try:
#             User.objects.get(username=username)
#         except User.DoesNotExist:
#             return username
#         raise forms.ValidationError(self.error_message['duplicate_username'])



@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','image')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


# @admin.register(User)
# class MyUserAdmin(AuthUserAdmin):
#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         print(form)
#         is_superuser = request.user.is_superuser
#         print("bhuban is "+str(is_superuser))
#         disabled_fields = set()  # type: Set[str]

#         if not is_superuser:
#             disabled_fields |= {
#                 'username',
#                 'is_superuser',
#             }

#         for f in disabled_fields:
#             if f in form.base_fields:
#                 form.base_fields[f].disabled = True

#         return form

#     readonly_fields = [
#        'last_login', 'date_joined', #'is_student','is_accountant', 'is_teacher','is_admin', 'is_principal',
#     ]
#     form = MyUserChangeForm
#     add_form = MyUserCreationForm
#     fieldsets = AuthUserAdmin.fieldsets + (
#         ('Extended Fields', {'fields': ('is_student','is_accountant', 'is_teacher','is_admin', 'is_principal')}),
#     )
#     list_display = ('email', 'is_student', 'is_teacher', 'is_accountant', 'is_admin', 'is_principal')
#     search_fields = ['email']



# class RegistrationAdmin(admin.ModelAdmin):
#     list_display = ['name', 'email']
#     search_fields = ['email']

# admin.site.register(Registration,RegistrationAdmin)