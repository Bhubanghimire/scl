from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Notice,Routine,Staff,ClassRoom,Subject,User,Staff_Leave_Application,User
from datetime import datetime
from .forms import AddStaff,AddRoutines,Newclass,Newsubjects,NewNotice,UserUpdateform
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from student.models import Attendance
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
# Create your views here.


@login_required()
def home(request):
    if request.user.is_admin:
        return render(request, 'administration/dashboard.html')
    elif request.user.is_student:
        return render(request,'student/dashboard.html')
    elif request.user.is_parent:
        return render(request,'parent/dashboard.html')
    elif request.user.is_teacher:
        return render(request,'teacher/dashboard.html')

    return render(request, 'administration/dashboard.html')

   

@csrf_exempt
@login_required()
def AddNotice(request):
    result=None
    if request.method == 'POST':
        form = NewNotice(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('notice_post')
        else:
            form = NewNotice()
            title=request.POST.get('title',"tiledefault")
            date=request.POST.get('date',"datedefault")
            
            notice_filtered= Notice.objects.filter(date=date, title=title).exists()
            if(not notice_filtered):
                result ="Sorry! Data not found"
                param = {'form': form,'result':result}
                return render(request, 'notice.html',param)
            notice_filtered= Notice.objects.filter(date=date, title=title).order_by('date')
            print(notice_filtered)
            form = NewNotice() 
            page = request.GET.get('page', 1)
            paginator = Paginator(notice_filtered, 7)
            try:
                topic = paginator.page(page)
            except PageNotAnInteger:
                topic = paginator.page(1)
            except EmptyPage:
                topic = paginator.page(paginator.num_pages)
            if topic.has_other_pages:
                print(topic)
            param={'form': form,'topics': topic}
            return render(request,'notice.html',param)
    else: 
        form = NewNotice() 

        notice=Notice.objects.all().order_by('-created_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(notice, 7)
        print("bhuban")
        try:
            topics = paginator.page(page)
        except PageNotAnInteger:
            topics = paginator.page(1)
        except EmptyPage:
            topics = paginator.page(paginator.num_pages)

        return render(request, 'notice.html',{'form': form,"noti":notice,'topics': topics})


@login_required()
def Map(request):
    return render(request,'map.html')



@login_required()
def ShowRoutine(request):
    result=None
    if request.method == "POST":
        room_no=request.POST.get('room')
        day=request.POST.get('day')
        clss=ClassRoom.objects.filter(room_number=room_no)
        print(clss)
        if(not clss):
            result="Sorry class room not found with that data"
            return render(request, 'routine.html',{'result': result})

        routine = Routine.objects.filter(Class=clss[0],day=day )
        if(not routine):
            result="Sorry routine not found with that data"
            return render(request, 'routine.html',{'result': result})
        else:
            obj =Routine.objects.filter(Class=clss[0], day=day )
            page = request.GET.get('page', 1)
            paginator = Paginator(obj, 10)
            try:
                topics= paginator.page(page)
            except PageNotAnInteger:
                topics = paginator.page(1)
            except EmptyPage:
                topics = paginator.page(paginator.num_pages)
            return render(request, 'routine.html',{'topics': topics})

    obj = Routine.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(obj, 3)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)

    return render(request, 'routine.html',{'topics': topics})


@csrf_exempt
@login_required()
def NewStaff(request):
    if request.method == 'POST':
        form = AddStaff(request.POST,request.FILES)
        if form.is_valid():
            gmail=form.cleaned_data['email']
            typeofemploye = form.cleaned_data['Type']
            p=request.POST.get('p')
            if p:
                if(typeofemploye=='Teacher'):
                    User.objects.create_user(username=gmail,email=gmail, password='somepass',is_teacher=True)

                if(typeofemploye=='Principle'):
                    User.objects.create_user(username=gmail,email=gmail, password='somepass',is_principal=True)
            
                if(typeofemploye=='Accountant'):
                    User.objects.create_user(username=gmail,email=gmail, password='somepass',is_accountant=True)
                if(typeofemploye=='Vice-Principle'):
                    User.objects.create_user(username=gmail,email=gmail, password='somepass',is_viceprinciple=True)
           
            
            form.save(commit=True)
            return redirect('home')
    else:
        form = AddStaff()
    
    return render(request, 'newstaff.html', {'form': form})



@login_required()
def AllStaff(request):
    result=None
    if request.method == "POST":
        name=request.POST.get('name')

        staff = Staff.objects.filter(name=name)
        if (not staff):
            result = "Staff Not Found.Please Enter  data"
            param={'result':result}
            return render(request,'administration/allstaff.html',param)
        else:
            obj=Staff.objects.filter(name=name).order_by('-name')
            param={"topics":obj}
            return render(request,'administration/allstaff.html',param)

    obj =  Staff.objects.all().order_by('-name')
    page = request.GET.get('page', 1)
    paginator = Paginator(obj, 5)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    param={"admission":obj,'topics': topics}
    return render(request,'administration/allstaff.html',param)



@csrf_exempt
@login_required()
def AddRoutine(request,id):
    clss_level = ClassRoom.objects.get(id=id)
    print(clss_level)
    teacher=Staff.objects.filter(Type="Teacher")
    subject=Subject.objects.filter(class_level=clss_level)
    print(subject)
    result=None
    if request.method == 'POST':
        form = AddRoutines(request.POST)
        if form.is_valid():
            teach = request.POST.get("teacher")
            sub = request.POST.get("subject")
            sub = Subject.objects.get(name=sub, class_level=clss_level)
            teach =Staff.objects.get(name=teach )
            instance=form.save(commit=False)
            print(instance.class_level)
            instance.class_level =clss_level
            instance.teacher = teach
            instance.subject = sub
            print(instance.class_level)
            instance.save()
            return redirect("routine")
    else:
        print("form not valid")
        form = AddRoutines()
        class_level=ClassRoom.objects.all()
    return render(request, 'newroutine.html', {'form': form,'teacher':teacher,'subject':subject})





@csrf_exempt
@login_required()
def Search_class(request):
    No=False
    if request.method == 'POST':
        class_name=request.POST.get("class")
        sec = request.POST.get("sec")
        print(sec)
        print(class_name)
        class_level = ClassRoom.objects.filter(class_level=class_name, section=sec)
        print(class_level)
        if class_level:
            class_level=ClassRoom.objects.get(class_level=class_name, section=sec)
            print(class_level)
            print(class_level.id)
            return redirect("addroutine", id=class_level.id)
        else:
            No="Enter Correct class and Section"
            classs = ClassRoom.objects.order_by().values_list('class_level').distinct()
            print("bhuban ghimire1")
            print(classs)
            class_level=[]
            for i in classs:
                for i in i:
                    class_level.append(i)
            print(class_level)
            class_sec = []
            class_section=ClassRoom.objects.order_by().values_list('section').distinct()
            for i in class_section:
                for i in i:
                    class_sec.append(i)

            class_sec=sorted(class_sec)

            return render(request, 'newroutine.html',{"no":No,"class_level":class_level,'class_section':class_sec})

   
    else:
        No="Select Existing class And sec"
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
    return render(request, 'newroutine.html',{"no":No,"class_level":class_level,'class_section':class_sec})




@csrf_exempt
@login_required()
def Addsubject(request):
    result=None
    cls_level =[]
    classs = ClassRoom.objects.order_by().values_list('class_level').distinct()
    for i in classs:
        for i in i:
            cls_level.append(i)

    if request.method == 'POST':
        form = Newsubjects(request.POST)
        print(form)
        if 'submit' in request.POST:
            if form.is_valid():
                class_level = request.POST.get("class")
                print(class_level)
                class_levels = ClassRoom.objects.filter(class_level=class_level).first()
                instance=form.save(commit=False)
                instance.class_level=class_levels
                print(instance.class_level)
                instance.save()
                print("dsjhaf")
                return redirect('addsubject')
            else:
                result="please enter correct book id."
                param={'form': form,'class_level':cls_level}
                return render(request,'administration/addsubject.html',param)

        if 'search' in request.POST:
            form = Newsubjects()
            bookid=request.POST.get('book',"default")


            book=Subject.objects.filter(book_ID=bookid)
            if(not book):
                result="Subject Not Found"
                param={'form': form,'result':result,'class_level':cls_level}
                return render(request,'administration/addsubject.html',param)

            param={'form': form,'topics': book,'class_level':cls_level}
            return render(request,'administration/addsubject.html',param)
            
    else: 
        form = Newsubjects() 
        cls_level =[]
        classs = ClassRoom.objects.order_by().values_list('class_level').distinct()
        for i in classs:
            for i in i:
                cls_level.append(i)

        allsubject= Subject.objects.all()

        page = request.GET.get('page', 1)
        paginator = Paginator(allsubject, 5)

        try:
            topics = paginator.page(page)
        except PageNotAnInteger:
            topics = paginator.page(1)
        except EmptyPage:
            topics = paginator.page(paginator.num_pages)
        param={'form': form,"subject":allsubject,'topics': topics,'class_level':cls_level, 'nbar': 'home'}
        return render(request,'administration/addsubject.html',param)

    form = Newsubjects()
    param={'form': form}
    return render(request,'administration/addsubject.html',param)


@login_required()
@csrf_exempt
def Addclass(request):
    result=None
    if request.method == 'POST':
        form = Newclass(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('addclass')
        else:
            form = Newclass()
            room_no=request.POST.get('room',"default")
            allclass= ClassRoom.objects.filter(room_number=room_no)
            if( not allclass):
                result="class not found"
                param={'form': form,'result':result}
                return render(request,'administration/addclass.html',param)

            param={'form': form,'topics': allclass}
            return render(request,'administration/addclass.html',param)
            

    else:
        form = Newclass()

        allclass = ClassRoom.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(allclass, 2)

        try:
            topics = paginator.page(page)
        except PageNotAnInteger:
            topics = paginator.page(1)
        except EmptyPage:
            topics = paginator.page(paginator.num_pages)
        param={'form': form,'topics': topics}
        return render(request,'administration/addclass.html',param)


from django.core.exceptions import ObjectDoesNotExist




@login_required()
def AttendanceRecord(request):
    result=None
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

    if request.method== 'POST':
        dates=request.POST.get("dateofattendance")
        class_l=request.POST["class"]
        section=request.POST['section']

    
        found=ClassRoom.objects.filter(class_level=class_l, section=section).exists()
        
        if found:
            clsss=ClassRoom.objects.filter(class_level=class_l, section=section)
            obj =Attendance.objects.filter(class_level=clsss[0],date_now=dates)
            param={"obj":obj,"class_level":class_level,'class_section':class_sec}
            return render(request, 'administration/attendance.html',param)
       
        else:
            result="Data Not Found"
            return render(request, 'administration/attendance.html',{'result':result})
           
    else:
        obj =Attendance.objects.all()
        
        param={"obj":obj,"class_level":class_level,'class_section':class_sec}
        return render(request, 'administration/attendance.html',param)


class SubjectEditView(UpdateView):
    model=Subject
    template_name = 'administration/subject_update.html'
    fields='__all__'
    

class SubjectDeltView(DeleteView):
    model=Subject
    success_url = reverse_lazy('addsubject')


class ClassEditView(UpdateView):
    model=ClassRoom
    template_name = 'administration/class_update.html'
    fields='__all__'
    

class ClassDeltView(DeleteView):
    model=ClassRoom
    success_url = reverse_lazy('home')


class StaffEditView(UpdateView):
    model= Staff
    template_name = 'administration/staff_update.html'
    fields='__all__'
    

class StaffDeltView(DeleteView):
    model=Staff
    success_url = reverse_lazy('home')


class AttendanceEditView(UpdateView):
    model= Attendance
    template_name = 'administration/Attendance_update.html'
    fields='__all__'
   

class AttendanceDeltView(DeleteView):
    model=Attendance
    success_url = reverse_lazy('home')



class Staff_leave(ListView):
    model = Staff_Leave_Application
    template_name = "administration/staff_leave_application_list.html"
    paginate_by = 9




def leave_approved(request,id):
    obj=Staff_Leave_Application.objects.get(pk=id)
    obj.approve ="Approved"
    obj.save()

    obj=Staff_Leave_Application.objects.all().order_by('received_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(obj, 9)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    param={'object_list': topics}
    return render(request,'administration/staff_leave_application_list.html',param)


def leave_rejected(request,id):
    obj=Staff_Leave_Application.objects.get(pk=id)
    obj.approve ="Rejected"
    obj.save()
    obj=Staff_Leave_Application.objects.all().order_by('received_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(obj, 9)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    param={'object_list': topics}
    return render(request,'administration/staff_leave_application_list.html',param)


class RoutineEditView(UpdateView):
    model= Routine
    template_name = 'administration/routine_update.html'
    fields='__all__'
    

class RoutineDeltView(DeleteView):
    model=Routine
    success_url = reverse_lazy('routine')


class UserList(ListView):
    model = User
    template_name = "administration/user_list.html"
    paginate_by = 9


def Staff_role(request,id):
    obj=User.objects.filter(id=id).first()
    print(obj)
    if not obj:
        return  HttpResponse("he is not user")
        
    form = UserUpdateform(request.POST or None, instance= obj)
    context= {'form': form}

    if form.is_valid():
        obj= form.save(commit= False)
        obj.save()
        return redirect('allstaff')

    else:
        context= {'form': form,'error': 'The form was not updated successfully. Please enter in a title and content'}
        return render(request,'administration/User_update.html' , context)



def  StaffDetailView(request,id):
    result=None
    staff=Staff.objects.get(id=id)
    email=staff.email
    user=User.objects.filter(email=email)
    if not user:
        result="Your account is not activated"
    else:
        user=User.objects.get(email=email)
    param={'staff':staff,'user':user,'result':result}
    return render(request, "administration/profile.html",param)



def UserActivate(request,id):
    staff=Staff.objects.get(id=id)
    gmail=staff.email
    typeofemploye =staff.Type
    result=None
    if(typeofemploye=='Teacher'):
        User.objects.create_user(username=gmail,email=gmail, password='somepass',is_teacher=True)

    if(typeofemploye=='Principle'):
        usr=User.objects.create_user(username=gmail,email=gmail, password='somepass',is_principal=True)
            
    if(typeofemploye=='Accountant'):
        usr=User.objects.create_user(username=gmail,email=gmail, password='somepass',is_accountant=True)
    if(typeofemploye=='Vice-Principle'):
        usr=User.objects.create_user(username=gmail,email=gmail, password='somepass',is_viceprinciple=True)
    
    print(usr.id)
           
    param={'staff':staff,'user':usr,'result':result}
    # return redirect('staff_detail',param)
    return render(request, "administration/profile.html",param)