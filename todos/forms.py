from django.forms import ModelForm
from todos.models import Todo

class AddTodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = '__all__'