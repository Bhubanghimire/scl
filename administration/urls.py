from django.urls import path,include
from .views import *
from django.conf.urls import url
urlpatterns = [
    path("", home, name="home"),

    path('map',Map, name='map'),
    path('notice/',AddNotice, name="notice_post"),
    
    path("class",Addclass,name="addclass"),
    path('class/<int:pk>/edit', ClassEditView.as_view(), name='class_edit'),
    path('class/<int:pk>/dlt', ClassDeltView.as_view(), name='class_delete'),

    path("subject", Addsubject, name="addsubject"),
    path('subject/<int:pk>/edit', SubjectEditView.as_view(), name='subject_edit'),
    path('subject/<int:pk>/dlt', SubjectDeltView.as_view(), name='subject_delete'),

    path('routine', ShowRoutine, name="routine"),
    path('routineadd',Search_class,name="search_class_for_routine"),
    path('addroutine/<int:id>', AddRoutine, name="addroutine"),
    path('routine/<int:pk>/edit', RoutineEditView.as_view(), name='routine_edit'),
    path('routine/<int:pk>/dlt', RoutineDeltView.as_view(), name='routine_delete'),

    path('allstaff',AllStaff, name="allstaff"),
    path('newstaff',NewStaff,name="newstaff"),
    path('staff/<int:id>/details',StaffDetailView,name="staff_detail"),
    path('staff/<int:pk>/edit', StaffEditView.as_view(), name='staff_edit'),
    path('staff/<int:pk>/dlt', StaffDeltView.as_view(), name='staff_delete'),
    path('staff<int:id>/role',Staff_role,name='user_role'),

    path('staff/leave',Staff_leave.as_view(),name='leave_application'),
    path('staff/leave/aprove/<int:id>',leave_approved,name='leave_approved'),
    path('staff/leave/rejected/<int:id>',leave_rejected,name='leave_rejected'),
    

    path('attendance',AttendanceRecord,name="attendance"),
    path('attendance/<int:pk>/edit', AttendanceEditView.as_view(), name='attendance_edit'),
    path('attendance/<int:pk>/dlt', AttendanceDeltView.as_view(), name='attendance_delete'),

    path('staff/<int:id>/detail',UserActivate, name='user_activate'),
    # path('user/<int:pk>/edit',UserEditView.as_view(), name='useredit'),
    
    
]