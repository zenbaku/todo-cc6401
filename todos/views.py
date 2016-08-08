from django.http import HttpResponse
from django.db import connection
from django.views.generic import ListView

from .models import Todo


class TodoList(ListView):
    model = Todo
