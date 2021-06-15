from django.urls import path
from .views import *


urlpatterns = [
    path('login/',login),
    path('notice/', NoticeAPIView.as_view()),
    path('class/',ClassAPIView.as_view()),
    
    path('leaveapply/',LeaveCreateAPIView),
    path('attendance/submit/',csrf_exempt(PostAttendanceAPIView.as_view())),
    path('leave/get/', LeaveAPIView.as_view({'get': 'list'})),
    path('attendance/search/', AttendaceAPIView.as_view()),

    # path('routine/',RoutineAPIView.as_view()),
    path('attendance/',AttendaceStudentAPIView.as_view()),

    path('logout/', Logout.as_view()),

    # path('subject/',SubjectApiVIew.as_view()),

    path('routine/',RoutineAPIView),
    
]
