from django.test import TransactionTestCase
from django.db import IntegrityError
from todos.models import Todo
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
