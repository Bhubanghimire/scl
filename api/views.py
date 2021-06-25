from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from student.models import Student,Attendance
from administration.models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.decorators import api_view
from administration.models import *

3


@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(email=email, password=password)
    print(user)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    usr= User.objects.filter(email=email, is_teacher=True).count()
    print(usr)
    if  usr>0:
        usr= User.objects.get(email=email, is_teacher=True)
        return Response({'token': token.key,'status':HTTP_200_OK,'id':usr.id},
                    status=HTTP_200_OK)
    return Response({'error': "You are not teacher"})

class NoticeAPIView(generics.ListAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer



class StudentAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer



from rest_framework import viewsets
class LeaveAPIView(viewsets.ModelViewSet):
    serializer_class = LeaveApplicationSerializer

    def get_queryset(self):
        gmail = self.request.user
        print(gmail)
        user=User.objects.get(username=gmail)
        queryset = Staff_Leave_Application.objects.filter(user=user)
        return queryset




@api_view(['POST',])
def LeaveCreateAPIView(request):
    serializer = LeaveApplicationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)





class AttendaceAPIView(generics.ListAPIView):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        teacher = self.request.user
        clas = self.request.data.get("class")
        sec =self.request.data.get("sec")
        day=self.request.data.get('date')

        teacher = Staff.objects.get(email=teacher, Type="Teacher")
        teacher = Teachers.objects.get(name=teacher)
        clss=ClassRoom.objects.get(class_level=clas, section=sec)
        queryset=Attendance.objects.filter(teacher=teacher,date_now=day, class_level=clss)
        return queryset
from student.models import Student

class AttendaceAPIView(generics.ListAPIView):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        teacher = self.request.user
        clas = self.request.data.get("class")
        day=self.request.data.get('date')
        sub=self.request.data.get('subject')
        print(day)

        teacher = Staff.objects.get(email=teacher, Type="Teacher")
        teacher = Teachers.objects.get(name=teacher)
        queryset=Attendance.objects.filter(teacher=teacher,date_now=day, class_level=clas)
        return (queryset)

from rest_framework.permissions import AllowAny

class PostAttendanceAPIView(generics.CreateAPIView):
    serializer_class = AAAA
    permission_classes = (AllowAny,)

    
class AttendaceStudentAPIView(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        teacher = self.request.user
        clas = self.request.data.get("class")
        admission=Admission.objects.filter(class_level=clas)
        print(admission)
        queryset = Student.objects.filter(student__in=admission)
        print(queryset)
        
        return (queryset)





class ClassAPIView(generics.ListAPIView):
    serializer_class = ClassRoomSerializer
    queryset = ClassRoom.objects.all()



@api_view(["GET","POST"])
@permission_classes((AllowAny,))
def RoutineAPIView(request):
    day = request.data.get("day",0)
    class_level =request.data.get("class_level",0)
    user=request.user
    print(class_level)
    print(day)

    teacher=Staff.objects.get(email=user, Type='Teacher') 
    teacher=Teachers.objects.get(name=teacher)
    print(teacher)
    if ((not day) and (not class_level)):
        print("11")
        routine=Routine.objects.filter(teacher=teacher)
    else:
        print("222")
        routine=Routine.objects.filter(teacher=teacher,day=day,Class=class_level)

    serializers =RoutineSerializer(routine,many=True)

    return Response(serializers.data)

 
class  AttendaceStudentAPIView(APIView):
    serializer_class = StudentSerializer

    def post(self, request):
        class_level = request.data.get("class_level")
        subject = request.data.get("subject")

        admission = Admission.objects.filter(class_level=class_level)
        print(admission)
        student=Student.objects.filter(student__in=admission)
        print(student)
        serializers = StudentSerializer(student,many=True)
        return Response(serializers.data)


from rest_framework import status
class Logout(APIView):
    def get(self, request, format=None):
        print(self.request.user.auth_token)
        request.user.auth_token.delete()
        return Response({'status':HTTP_200_OK})