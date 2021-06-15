from django.urls import path,include
from django.conf.urls import url
# from allauth.account.views import LoginView, SignupView,LogoutView,PasswordChangeView,PasswordResetView,ConfirmEmailView, EmailVerificationSentView 
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('signup/',SignupView , name='signup'),   
    path('login/', LoginView, name="login"),
    path('logout/',Logout, name="logout"),
    # path('accounts/password/change/', PasswordChangeView.as_view(), name='account_change_password'),
    # path('accounts/password/reset/',PasswordResetView.as_view(), name='account_reset_password'),
    # url(r'^accounts/account-confirm-email/(?P<key>[-:\w]+)/$'   ,ConfirmEmailView.as_view(),name='account_confirm_email'),
    # path('accounts/account-verification/',EmailVerificationSentView .as_view(),name='account_email_verification_sent'),
    # path('relogin/', Inactive, name="account_inactive"),
]
