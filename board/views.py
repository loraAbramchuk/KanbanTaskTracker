from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Project
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import ProjectForm, TaskForm
from django.shortcuts import get_object_or_404
from .models import Task
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    return render(request, 'board/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('project_list')
    else:
        form = UserCreationForm()
        return render(request, 'board/register.html', {'form': form})

@login_required
def project_list(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'board/project_list.html', {'projects': projects})

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'board/create_project.html', {'form': form})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    tasks = project.tasks.all()
    return render(request, 'board/project_detail.html', {
        'project': project,
        'todo': tasks.filter(status='todo'),
        'inprogress': tasks.filter(status='in_progress'),
        'done': tasks.filter(status='done'),
    })

@login_required
def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', project_id=project.id)
        else:
            print(form.errors)
    else:
        form = TaskForm()
    return render(request, 'board/add_task.html', {'form': form, 'project': project})

@login_required
def move_task(request, task_id, new_status):
    task = get_object_or_404(Task, id=task_id, project__owner=request.user)

    if new_status in dict(Task.STATUS_CHOICES):
        task.status = new_status
        task.save()

    return redirect('project_detail', project_id=task.project.id)


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__owner=request.user)
    project_id = task.project.id
    task.delete()
    messages.success(request, "Задача удалена.")
    return redirect('project_detail', project_id=project_id)


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Задача обновлена.")
            return redirect('project_detail', project_id=task.project.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'board/edit_task.html', {'form': form, 'task': task})

@login_required
@csrf_exempt
def update_task_status(request, task_id):
    if request.method('POST'):
        task = get_object_or_404(Task, id=task_id, project__owner=request.user)
        new_status = request.POST.get('status')

        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
            return JsonResponse({'status': 'success', 'new_status': new_status})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid status'}, status=400)
