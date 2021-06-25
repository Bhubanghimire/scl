from django.shortcuts import render
from django.shortcuts import redirect
from .forms import ParentForm
from .models import Parent
from student.models import Student
from django.views.generic.detail import DetailView
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from administration.decorators import student_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from administration.models import User
from administration.forms import UserUpdateform
from django.http import HttpResponse

# Create your views here.
def Parentts(request):
    result =None
    if request.method == "POST":
        fathername=request.POST.get('fathername')
        mothername=request.POST.get('mothername')
        parent = Parent.objects.filter(father_name=fathername,mother_name=mothername)

        if (not parent):
            result = "Parent Not Found.Please Enter data"
            param={'result':result}
            return render(request,'parent/allparents.html',param)
        else:
            obj=Parent.objects.filter(father_name=fathername,mother_name=mothername)
            param={"topics":obj}
            return render(request,'parent/allparents.html',param)

    obj = Parent.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(obj, 4)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    param={"admission":obj,'topics': topics}
    return render(request,'parent/allparents.html',param)



@csrf_exempt
def Addparent(request):
    if request.method == 'POST':
        print(request.POST)
        form = ParentForm(request.POST,request.FILES)
        print(form.is_valid())
        if form.is_valid():
            gmail=form.cleaned_data['email']
            User.objects.create_user(email=gmail, password='somepass',is_parent=True)

            form.save(commit=True)
            return redirect('home')
    else:
        form = ParentForm()
    return render(request, 'parent/addparent.html', {'form': form})



def ParentDetail(request,pk):
    result=None
    parent=Parent.objects.get(id=pk)
    email=parent.email
    user=User.objects.filter(email=email)
    if not user:
        result="Your account is not activated"
    else:
        user=User.objects.get(email=email)
    param={'staff':parent,'user':user,'result':result}
    return render(request,'parent/profile.html',param)



class StudentEditView(UpdateView):
    model=Parent
    template_name = 'parent/parent_edit.html'
    fields='__all__'
   

class StudentDeltView(DeleteView):
    model=Parent
    success_url = reverse_lazy('home')

from django.contrib import messages

def Parent_Role(request,id):
    p=Parent.objects.get(id=id)
    email=p.email
    obj=User.objects.filter(email=email).first()
    print(obj)
    if not obj:
        return  HttpResponse("he is not user")
        
    form = UserUpdateform(request.POST or None, instance= obj)
    context= {'form': form}

    if form.is_valid():
        obj= form.save(commit= False)
        obj.save()
        topics =Parent.objects.all()
        param={"admission":obj,'topics': topics}

        return render(request, 'parent/allparents.html', param)

    else:
        context= {'form': form,'error': 'The form was not updated successfully. Please enter in a title and content'}
        return render(request,'administration/User_update.html' , context)

def UserActivate(request,id):
    parent=Parent.objects.get(id=id)
    gmail=parent.email
    result=None
    # if(typeofemploye=='Teacher'):
    usr=User.objects.create_user(email=gmail, password='somepass',is_parent=True)

    # if(typeofemploye=='Principle'):
    #     usr=User.objects.create_user(username=gmail,email=gmail, password='somepass',is_principal=True)
            
    # if(typeofemploye=='Accountant'):
    #     usr=User.objects.create_user(username=gmail,email=gmail, password='somepass',is_accountant=True)
    # if(typeofemploye=='Vice-Principle'):
    #     usr=User.objects.create_user(username=gmail,email=gmail, password='somepass',is_viceprinciple=True)
    
    print(usr.id)
           
    param={'staff':parent,'user':usr,'result':result}
    # return redirect('staff_detail',param)
    return render(request, "administration/profile.html",param)