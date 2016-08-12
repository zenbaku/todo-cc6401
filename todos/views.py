from django.shortcuts import redirect
from django.views.generic import ListView
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.views.generic import TemplateView, DetailView
from .models import Todo
from .forms import TodoForm

class AddTaskView(TemplateView):
    template_name = 'todos/add_task.html'
    form = None

    def get_context_data(self, **kwargs):
        context = super(AddTaskView, self).get_context_data(**kwargs)
        context['form'] = TodoForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TodoForm(request.POST)
        if form.is_valid():
            #agregar la tarea jeje
            form.save()
            #agregar mensaje
            messages.success(request, 'Task added successfully.')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Invalid Form, try again.')

class EditTaskView(DetailView):
    model = Todo
    template_name = 'todos/edit_task.html'
    form = None

    def get_context_data(self, **kwargs):
        context = super(EditTaskView, self).get_context_data(**kwargs)
        context = self.update_context(context, TodoForm)
        return context

    def post(self, request, *args, **kwargs):
        return self.update_post(request, TodoForm)

    def update_context(self, context, form):
        context['form'] = form(instance=self.object)
        return context

    def update_post(self, request, form):
        form = form(request.POST, instance=self.get_object())
        if form.is_valid():
            #agregar la tarea jeje
            form.save()
            #agregar mensaje
            messages.success(request, 'Task updated successfully.')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Invalid Form, try again.')


class TodoList(ListView):
    model = Todo


class UncompletedTodoList(ListView):
    template_name = 'todo_list.html'
    context_object_name = 'todo_list'

    def get_queryset(self):
        return Todo.objects.filter(is_completed=False)


def complete_task(request):
    """Mark a task as completed."""
    todo_id = request.POST.get('id')
    if todo_id:
        todo = Todo.objects.get(pk=todo_id)
        todo.is_completed = True
        todo.save()

    return redirect('TodoList')


def reorder_task(request):
    """Mark a task as completed."""
    todo_id = int(request.POST.get('id'))
    new_index = int(request.POST.get('new_index'))

    todo = Todo.objects.get(pk=todo_id)
    todo.to(new_index)

    return HttpResponse(status=200)
