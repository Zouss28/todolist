from django.shortcuts import render, get_object_or_404,redirect
from .models import Task
from .forms import TaskForm
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import logout,login
from django.contrib import messages
from django.core.exceptions import PermissionDenied

# Create your views here.

def access_control(obj, request):
    if obj.user != request.user:
        raise PermissionDenied("You are not allowed to edit this task.")

@login_required
def task_list(request):
    tasks = Task.objects.filter(user = request.user)
    return render(request, 'tasks/tasks_list.html',{'tasks':tasks})

def task_detail(request,pk):
    detail = get_object_or_404(Task,pk = pk)
    access_control(detail, request)
    return render(request,'tasks/task_detail.html',{'detail':detail})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(False)
            task.user = request.user
            task.save()
            return redirect('list')
    else:
        form = TaskForm()
        return render(request,'tasks/task_form.html',{'form':form})

def update_task(request,pk):
    task = get_object_or_404(Task,pk=pk)
    access_control(request, task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:  
        form = TaskForm(instance=task)
        return render(request,'tasks/task_form.html',{'form':form})
    
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    access_control(request, task)
    if request.method == 'POST':
        task.delete()
        return redirect('list')
    return render(request,'tasks/task_confirm_delete.html',{'detail':task})


def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    return JsonResponse({'Completed':task.completed})

#signup View
def signup_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request,f'Well done {form.get_user()} your account was Created !')
        return redirect('list')
    return render(request,'registration/signup.html',{'form':form})

def logout_view(request):
    logout(request)
    messages.info(request,f'You have been logged out.')
    return redirect('list')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            messages.success(request,f'Welcome back, {user.username}!')
            return redirect('list')
    else:
        form = AuthenticationForm()
    return render(request,'registration/login.html',{'form':form})
    