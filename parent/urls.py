from django.urls import path,include
from .views import *

urlpatterns = [
    path('Addparent',Addparent,name="addparent"),
    path('allparent',Parentts,name='allparent'),
    path("parentdetails/<int:pk>",ParentDetail,name="parent_details"),
    path('parent/<int:pk>/edit', StudentEditView.as_view(),name='parent_edit'),
    path('<int:pk>/dlt',StudentDeltView.as_view(),name='parent_delete'),
    path('parent/<int:id>/role',Parent_Role,name="parent_role"),
    path('parent/<int:id>/activate',UserActivate, name="parent_Account")
]