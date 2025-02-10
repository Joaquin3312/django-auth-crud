from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# def login(request):
#     return render(request, 'login.html',{
#         'form' : UserCreationForm
#     })
    
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == "GET":
         return render(request, 'signup.html',{
        'form' : UserCreationForm
    })
    else: #si es POST...
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                login(request,user)
                print("usuario creado, redireccinoando a tasks....")
                return redirect('home')
            except IntegrityError: 
                return render(request, 'signup.html' ,{
                    'form' : UserCreationForm,
                    'error' : 'User already exists'
                })
        return render(request, 'signup.html',{
            'form' : UserCreationForm,
            'error' : 'Password error, please try again'
        })


@login_required      
def tasks(request):
    tasks = Task.objects.filter(user=request.user,date_completed__isnull = True) #filtrar siempre desde la consulta y no en la vista (template)
    return render(request, 'tasks.html',{
        'tasks' : tasks
    })


@login_required
def task_detail(request,id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=id, user=request.user) #obtenemos un task específico por su id y del usuario
        form = TaskForm(instance=task) # pasamos task especifico para poder editarlo
        return render(request, 'task_detail.html',{
            'task' : task,
            'form' : form
        })
    else: #si es POST:
        try:
            task = get_object_or_404(Task, pk=id, user=request.user) #obtenemos el id
            form = TaskForm(request.POST, instance=task) #a través de instance pasamos el id y luego guardamos
            if form.is_valid():
                task.save()
                return redirect('tasks')
            else:
                return render(request, 'task_detail.html', {
                    'form': form,
                    'error': 'Form is not valid'
                })
        except Exception as e:
            return render(request, 'task_detail.html', {
                'form': TaskForm(),
                'error': str(e)
            })


@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm()
        })
    else:  # si es POST
        try:
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                return redirect('tasks')
            else:
                return render(request, 'create_task.html', {
                    'form': form,
                    'error': 'Form is not valid'
                })
        except Exception as e:
            return render(request, 'create_task.html', {
                'form': TaskForm(),
                'error': str(e)
            })
            
@login_required        
def task_delete(request, id):
    task = get_object_or_404(Task, pk=id)
    task.delete()
    return redirect('tasks')


@login_required
def task_complete(request,id):
    task = get_object_or_404(Task,pk=id, user=request.user)
    try:
        if request.method == 'POST':
            task.completed = True 
            task.date_completed = timezone.now()
            task.save()
            return redirect('tasks')
    except Exception as e:
        return redirect ('task',{
            'error' : 'error al eliminar task'
        })
    
    
@login_required
def list_tasks_completed (request):
    tasks_completed = Task.objects.filter(user= request.user,date_completed__isnull = False).order_by('-date_completed') # uso de field Lookup: "__isnull"
    return render(request, 'tasks_completed.html',{
        'tasks_completed' : tasks_completed
    })


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


#ESTAMOS EL LOGIN METHOD "sigin"
def user_login(request):
    if request.method == "GET":
        return render(request, 'login.html', {
            'form': AuthenticationForm()
        })
    else: # si es POST
        user = authenticate(request, username=request.POST['username'],password= request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm(),
                'error': 'Invalid username or password'
            })
        else:
            login(request,user)
            return redirect('home')

        
    
        
