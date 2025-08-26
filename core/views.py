from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Task

# Create your views here.
    
#avoir la date du jour
def get_today():
    return timezone.now().strftime('%d/%m/%Y')


##################################################################
# logique des pages

# page home
def home(request):
    context = {
        'today': get_today(),
    }
    return render(request, 'pages/home.html', context)

# page about
def about(request):
    context = {
        'today': get_today(),
    }
    return render(request, 'pages/about.html', context)

# page task_list
def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    context = {
        'today': get_today(),
        'tasks': tasks,
        'total_tasks': tasks.count(),
        'completed_tasks': tasks.filter(completed=True).count(),
        'active_tasks': tasks.filter(completed=False).count(),
    }
    return render(request, 'pages/task_list.html', context)

# page task_active
def task_active(request):
    tasks = Task.objects.filter(completed=False).order_by('-created_at')
    context = {
        'today': get_today(),
        'tasks': tasks,
        'total_tasks': Task.objects.count(),
        'completed_tasks': Task.objects.filter(completed=True).count(),
        'active_tasks': tasks.count(),
    }
    return render(request, 'pages/task_active.html', context)

# page task_detail
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    context = {
        'today': get_today(),
        'task': task,
    }
    return render(request, 'pages/task_detail.html', context)
