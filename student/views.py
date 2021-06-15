from django.shortcuts import render
from django.http import HttpResponse
from .models import Student
from parent.forms import ParentForm
from administration.forms import StudentAdmission
from administration.models import ClassRoom,Admission,User
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from parent.models import Parent
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


# Create your views here.
@csrf_exempt
def NewAdmission(request): 
    
    result=None  
    if request.method == 'POST':
        formS = StudentAdmission(request.POST,request.FILES)
        chebox=request.POST.get("optradio")


        if ((chebox=="YES" or chebox=="NO") and formS.is_valid()):
            p = formS.save()
            permission=request.POST.get("p")
            if permission:
                gmail=formS.cleaned_data['email']
                User.objects.create_user(username=gmail,email=gmail, password='somepass',is_student=True)

            if chebox=="YES":
                return redirect('parent_exists')
            else:
                return redirect('parent_not_exists')            
            
        else:
            result="Sorry You entered wrong data."
            formS = StudentAdmission(request.POST,request.FILES)
            context = {
                    'result':result,
                    'formS':formS
                    }
            
            return render(request, 'student/NewAdmission.html', context)

    formS = StudentAdmission()
    context = {
        'formS':formS,
    }
    return render(request, 'student/NewAdmission.html', context)


class Students(ListView):
    model = Student
    template_name = "student/Allstudents.html"
    paginate_by = 10

    
    def get_queryset(self):
        name = self.request.GET.get('name', '')
        object_list = self.model.objects.all().order_by('student')
        
        if name:      
            student=Admission.objects.filter(name=name)
            if student:
                object_list=Student.objects.filter(student=student[0])
                return object_list
            else:
                object_list=Student.objects.none()
                return object_list
        return object_list


from student.models import Attendance
from datetime import datetime, timedelta

class DetailStudent(DetailView):
    model = Student
    # context_object_name = 'stu_detail' 
    template_name ='student/DetailStudent.html'

    def get_context_data(self, *args, **kwargs):
        
        context = super(DetailStudent, self).get_context_data(*args, **kwargs)
        print(context)
        stu=Student.objects.get(id=self.kwargs.get('pk'))
        print(stu)
        today = datetime.now()
        six_days_ago_date = (today - timedelta(days=7)).date()
        context['attendance'] = Attendance.objects.filter(student=stu,date_now__gte=six_days_ago_date)
        print(context['attendance'])
        for i in context['attendance']:
            print(i)
        print(context)

        return context



class StudentEditView(UpdateView):
    model=Admission
    template_name = 'student/student_update.html'
    fields='__all__'



class StudentDeltView(DeleteView):
    model=Student
    success_url = reverse_lazy('home')



def Promotion(request):
    result=""
    param={}
    class_level = []
    class_levels=ClassRoom.objects.order_by().values_list('class_level').distinct()
    for i in class_levels:
        for i in i:
            class_level.append(i)
    class_sec = []
    class_section=ClassRoom.objects.order_by().values_list('section').distinct()
    for i in class_section:
        for i in i:
            class_sec.append(i)

    class_sec=sorted(class_sec)


    if request.method=="POST":
        regno= request.POST.get("regno")
        new_class = request.POST.get("class")
        new_sec = request.POST.get("Section")
        new_roll = request.POST.get("roll")

        
        student_Check = Admission.objects.filter(registration_no=regno).first()
        if(not student_Check):
            result="Sorry!! student doesnot exists."
            param={"result":result,'class_level':class_level,'class_sec':class_sec}
            return render(request,'administration/Student_Promotion.html',param)

        roll_Check =True
        try:
            clss = ClassRoom.objects.get(class_level=new_class, section=new_sec)
        except ClassRoom.DoesNotExist:
                result="Sorry!! class doesnot exists."
                param={"result":result,'class_level':class_level,'class_sec':class_sec}
                return render(request,'administration/Student_Promotion.html',param)
        else:
            roll_Check = Admission.objects.filter(class_level=clss, roll_no=new_roll).first()
       
        if(student_Check and not roll_Check):
            stu = Admission.objects.get(registration_no=regno)
            stu.class_level = clss
            stu.roll_no = new_roll
            result="Succcessfully Promotted"
            stu.save()
        else:
            result="Sorry! Roll No already exists."
            param={"result":result,'class_level':class_level,'class_sec':class_sec}
            return render(request,'administration/Student_Promotion.html',param)
    param={"result":result,'class_level':class_level,'class_sec':class_sec}
    return render(request,'administration/Student_Promotion.html',param)



def Parentform(request):
    if request.method=="POST":
        form=ParentForm(request.POST,request.FILES)
        print(form.is_valid())
        
        if form.is_valid():
            p=form.save()
            gmail=form.cleaned_data['email']
            permission=request.POST.get('p')
            if permission:
                User.objects.create_user(username=gmail,email=gmail, password='somepass',is_parent=True)

            stu=Admission.objects.last()
            s=Student.objects.create()
            s.student.add(stu)
            s.parent.add(p)
            
            return redirect('allstudent')

        else:
            result="Sorry You entered wrong data."
            form = ParentForm(request.POST,request.FILES)
            context = {
                    'result':result,
                    'form':form
                    }
            
            return render(request, 'administration/parentinfo.html', context)

    form = ParentForm()

    context = {
        'form':form,
    }
    return render(request, 'administration/parentinfo.html', context)



def Parentselect(request):
    result=None
    if request.method=="POST":
        father_name = request.POST.get("name")
        email = request.POST.get("email")
        phone =  request.POST.get("phone")
        print(father_name)
        print(email)
        print(phone)
        count=Parent.objects.filter(name=father_name,email=email,contact=phone ).count()
        
        if  count==0:
            result= "old parent information not found"
            return render(request, 'administration/search_parent.html',{'result1':result})
        else:
            result="Following data is added"
            p=Parent.objects.get(name=father_name,email=email,contact=phone )
            stu=Admission.objects.last()
            s=Student.objects.create()
            s.student.add(stu)
            s.parent.add(p)
            return redirect('allstudent')
            # return render(request, 'administration/search_parent.html',{'result':result,'parent':p})
   

    return render(request, 'administration/search_parent.html')


def AddParent(request,id):
    stu=Student.objects.get(id=id)
    if request.method=="POST":
        form=ParentForm(request.POST,request.FILES)
        print(form.is_valid())
        
        if form.is_valid():
            p=form.save()
            gmail=form.cleaned_data['email']
            permission=request.POST.get('p')
            if permission:
                User.objects.create_user(username=gmail,email=gmail, password='somepass',is_parent=True)

            stu.parent.add(p)
            
            return redirect('student_detail',pk=id)

        else:
            result="Sorry You entered wrong data."
            form = ParentForm(request.POST,request.FILES)
            context = {
                    'result':result,
                    'form':form
                    }
            
            return render(request, 'administration/parentinfo.html', context)

    form = ParentForm()

    context = {
        'form':form,
    }
    return render(request, 'administration/parentinfo.html', context)
