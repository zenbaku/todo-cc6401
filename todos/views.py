from django.shortcuts import redirect
from django.views.generic import ListView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Todo
from .forms import AddTodoForm

def add_todo(request):
    if request.method == 'POST':
        form = AddTodoForm(request.POST)
        if form.is_valid():
            #agregar la tarea jeje
            form.save()
            #agregar mensaje
            messages.success(request, 'Task Added Successfully.')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Not Valid Form :(')
            return HttpResponseRedirect('/')
    else:
        form = AddTodoForm()
    return render(request, 'todos/add_todo.html', {'form': form})

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
