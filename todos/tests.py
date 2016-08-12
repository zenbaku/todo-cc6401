from django.test import TransactionTestCase
from django.db import IntegrityError
from todos.models import Todo
from todos.forms import AddTodoForm
from django.test import Client


class TodoTestCase(TransactionTestCase):
    def setUp(self):
        Todo.objects.create(description='My first todo!')
        Todo.objects.create(description='My second todo', is_completed=True)

    def test(self):
        first = Todo.objects.first()
        second = Todo.objects.last()

        self.assertFalse(first.is_completed)
        self.assertTrue(second.is_completed)

    def test_null_description(self):
        with self.assertRaises(IntegrityError):
            Todo.objects.create(description=None)


class ViewListTestCase(TransactionTestCase):
    def setUp(self):
        self.c = Client()
        self.description = 'My first todo!'
        Todo.objects.create(description=self.description)

    def test(self):
        response = self.c.get('/')
        self.assertIn(self.description, response.content)


class CompleteTaskTestCase(TransactionTestCase):
    def setUp(self):
        self.c = Client()
        self.todo = Todo.objects.create(
            description='Hello',
            is_completed=False
        )

    def test_complete_button_present(self):
        response = self.c.get('/')
        self.assertIn('completar', response.content)

    def test_complete_task(self):
        todo_id = self.todo.id

        response = self.c.post('/complete/', {
            'id': todo_id
        })

        todo = Todo.objects.get(pk=todo_id)
        self.assertTrue(todo.is_completed)
        self.assertNotIn('completar', response.content)

class AddTaskTestCase(TransactionTestCase):
    def setUp(self):
        self.c = Client()
        self.form_data = {'description': 'test task', 'is_completed' : True}

    def test_form_valid(self):
        form = AddTodoForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_post_data(self):
        response = self.c.post('/add_todo/', self.form_data, follow=True) #follow sigue redirects
        self.assertTrue(response.status_code == 200)
        index = self.c.get('/')
        self.assertIn(self.form_data['description'], index.content)
