from django.db import models
from administration.models import Admission, ClassRoom,User,Subject,Staff
# from teacher.models import Teachers
from parent.models import Parent
from django.urls import reverse


# Create your models here.
class Student(models.Model):
    student = models.ManyToManyField(Admission,related_name="student", blank=True )
    parent = models.ManyToManyField(Parent, related_name="parent", blank=True)
    

    def __str__(self):
        studentname = ", ".join(str(seg) for seg in self.student.all())
        return studentname

        

class Attendance(models.Model):
    status_Choice=(("P","P"),("A","A"))
    student = models.ForeignKey(Student , on_delete=models.SET_NULL,null=True, related_name="attendance")
    class_level = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL,null=True)
    teacher = models.ForeignKey(Staff, on_delete=models.SET_NULL,null=True,related_name="teacherforattendance")
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL,null=True)
    date_now = models.DateField(auto_now=True)
    status = models.CharField(max_length=5,choices=status_Choice,default="")


    def __str__(self):
        return self.class_level.class_level


    def get_absolute_url(self):
        return reverse('attendance')