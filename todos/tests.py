from django.test import TransactionTestCase
from django.db import IntegrityError
from todos.models import Todo


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
