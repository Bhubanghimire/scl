# from django.shortcuts import render,redirect
# from .models import Teachers
# from .forms import TeacherForm
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.db.models import Count
# from django.views.decorators.csrf import csrf_exempt
# from django.views.generic.edit import CreateView,UpdateView,DeleteView
# from django.urls import reverse_lazy
# from django.views.generic.detail import DetailView
# from administration.models import Staff


# @csrf_exempt
# def AllTeachers(request):
#     result =None
#     if request.method == 'POST':
#         form=TeacherForm(request.POST)
#         if form.is_valid():
#             form.save(commit=True)
#             return redirect('allteacher')
#         else:
#             firstname=request.POST.get('firstname')
#             lastname=request.POST.get('lastname')
#             staff=Staff.objects.filter(first_name=firstname,last_name=lastname)

#             if(not staff):
#                 result = "staff with that email Not Found.Please Enter  data"
#                 param={'form': form,'result':result}
#                 return render(request,'teacher/allteacher.html',param)

#             teacher = Teachers.objects.filter(name=staff[0])
#             if (not teacher):
#                 result = "teacher Not Found.Please Enter  data"
#                 param={'form': form,'result':result}
#                 return render(request,'teacher/allteacher.html',param)
#             else:
#                 obj=Teachers.objects.filter(name=staff[0])
#                 page = request.GET.get('page', 1)
#                 paginator = Paginator(obj, 2)
#                 try:
#                     topics = paginator.page(page)
#                 except PageNotAnInteger:
#                     topics = paginator.page(1)
#                 except EmptyPage:
#                     topics = paginator.page(paginator.num_pages)
#                 param={'form': form,"topics":topics}
#                 return render(request,'teacher/allteacher.html',param)

#     else:
#         form=TeacherForm()
#     obj = Teachers.objects.all()

#     page = request.GET.get('page', 1)
#     paginator = Paginator(obj, 2)

#     try:
#         topics = paginator.page(page)
#     except PageNotAnInteger:
#         topics = paginator.page(1)
#     except EmptyPage:
#         topics = paginator.page(paginator.num_pages)
#     param={'form': form,'topics': topics}

#     return render(request,'teacher/allteacher.html',param)


# class DetailTeacher(DetailView):
#     model = Teachers
#     context_object_name = 'teacher' 
#     template_name ='teacher/DetailTeacher.html'



# class TeacherDeltView(DeleteView):
#     model=Teachers
#     success_url = reverse_lazy('home')
