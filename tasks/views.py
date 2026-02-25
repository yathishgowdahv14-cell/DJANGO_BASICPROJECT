from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Task
from .forms import TaskForm


def dashboard(request):
    tasks = Task.objects.all()

    # Filters
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    category_filter = request.GET.get('category', '')

    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    if category_filter:
        tasks = tasks.filter(category=category_filter)

    # Stats
    all_tasks = Task.objects.all()
    total = all_tasks.count()
    done = all_tasks.filter(status='done').count()
    in_progress = all_tasks.filter(status='in_progress').count()
    todo = all_tasks.filter(status='todo').count()
    today = timezone.now().date()
    overdue = sum(1 for t in all_tasks if t.is_overdue)

    context = {
        'tasks': tasks,
        'total': total,
        'done': done,
        'in_progress': in_progress,
        'todo': todo,
        'overdue': overdue,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'category_filter': category_filter,
    }
    return render(request, 'tasks/dashboard.html', context)


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Create Task'})


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Edit Task'})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    # Cycle: todo -> in_progress -> done -> todo
    cycle = {'todo': 'in_progress', 'in_progress': 'done', 'done': 'todo'}
    task.status = cycle.get(task.status, 'todo')
    task.save()
    return redirect('dashboard')
