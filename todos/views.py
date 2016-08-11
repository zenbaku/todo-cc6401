from django.shortcuts import redirect
from django.views.generic import ListView

from .models import Todo


class TodoList(ListView):
    model = Todo


def complete_task(request):
    """Mark a task as completed."""
    todo_id = request.POST.get('id')
    if todo_id:
        todo = Todo.objects.get(pk=todo_id)
        todo.is_completed = True
        todo.save()

    return redirect('TodoList')
