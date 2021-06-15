from django.urls import path,include
from .views import *

urlpatterns = [
    path("allstudent",Students.as_view(),name='allstudent'),
    path('addstudent',NewAdmission,name="addstudent"),
    path('selectparent',Parentselect,name="parent_exists"),
    path('newparent',Parentform,name="parent_not_exists"),
    path('detailstudent/<int:pk>',DetailStudent.as_view(),name="student_detail"),
    path('student/<int:pk>/edit', StudentEditView.as_view(),name='student_edit'),
    path('student/<int:pk>/dlt',StudentDeltView.as_view(),name='student_delete'),
    path('promotion',Promotion,name="student_promotion"),
    path('parentadd/<int:id>',AddParent,name="parent_add"),
]