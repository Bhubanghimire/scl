from rest_framework import serializers
from parent.models import Parent
from student.models import Student,Attendance
from administration.models import *


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notice
        fields=['id','title','created_at','postby','detail']

class SubjectSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Subject
        fields = ['id','name','class_level']


class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model= ClassRoom
        fields=['id','class_level','section']
    

    
class LeaveApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Staff_Leave_Application
        fields=['id','user','reason','leave_type','startdate','endate','approve']



class RoutineSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    Class = ClassRoomSerializer(read_only=True)


    class Meta:
        model= Routine
        fields = ['Class','day','start_time','subject','end_time']





class AdmissionSerializer(serializers.ModelSerializer):
    class_level = ClassRoomSerializer(read_only=True)
    class Meta:
        model = Admission #(name=..., dob=..., phone=..., address=..., email=..., =..., gender=..., district=..., sesson=..., roll_no=..., registration_no=..., join_date=...)
        fields= ("name",  'class_level', "roll_no",)





class StudentSerializer(serializers.ModelSerializer):
    student =AdmissionSerializer(read_only=True,many=True)
    class Meta:
        model = Student
        fields = ['id','student']



class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    subject=SubjectSerializer(read_only=True)
    roll_no =serializers.CharField(source='student.roll_no', read_only=True)
    class_level=ClassRoomSerializer(read_only=True)

    class Meta:
        model= Attendance
        fields=['student','roll_no','class_level','subject','status']
        extra_kwargs = {'student': {'required': False}}

    def create(self, validated_data):
        return validated_data





class AAAA(serializers.ModelSerializer):
    section=serializers.CharField(source='class_level.section', read_only=True)
    

    class Meta:
        model= Attendance
        fields=['id','student','class_level','teacher','section','subject','status']


