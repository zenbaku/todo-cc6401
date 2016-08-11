from django.views.generic import ListView

from .models import Todo


class TodoList(ListView):
    model = Todo
