from django.test import TransactionTestCase
from django.db import IntegrityError
from todos.models import Todo
from todos.forms import TodoForm
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
        
class DeleteTaskTestCase(TransactionTestCase):
    def setUp(self):
        self.c = Client()
        self.todo = Todo.objects.create(
            description='Hello',
            is_completed=False
        )

    def test_delete_button_present(self):
        response = self.c.get('/')
        self.assertIn('eliminar', response.content)

    def test_delete_task(self):
        todo_id = self.todo.id

        response = self.c.post('/delete/', {
            'id': todo_id
        })
        
        try:
            todo = Todo.objects.get(pk=todo_id)
        except:
            todo = None
        self.assertIsNone(todo)

class AddTaskTestCase(TransactionTestCase):
    def setUp(self):
        self.c = Client()
        self.form_data = {'description': 'test task', 'is_completed' : True}

    def test_form_valid(self):
        form = TodoForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_post_data(self):
        response = self.c.post('/add_task/', self.form_data, follow=True) #follow sigue redirects
        self.assertTrue(response.status_code == 200)
        index = self.c.get('/')
        self.assertIn(self.form_data['description'], index.content)


class EditTestCase(TransactionTestCase):
    def setUp(self):
        self.c = Client()
        self.form_data = {'description': 'test task', 'is_completed' : True}
        self.edited_form_data = {'description':'edited test task', 'is_completed' : False}
        self.c.post('/add_task/', self.form_data, follow=True) #agrega usando add_task

    def test_edit_post_data(self):
        first = Todo.objects.first()
        response = self.c.post('/edit_task/'+str(first.pk)+'/', self.edited_form_data, follow=True) #follow sigue redirects
        self.assertTrue(response.status_code == 200)
        index = self.c.get('/')
        self.assertIn(self.edited_form_data['description'], index.content)


class OrderTaskTestCase(TransactionTestCase):
    def setUp(self):
        self.first = Todo.objects.create(description='first!')
        self.second = Todo.objects.create(description='second')
        self.third = Todo.objects.create(description='third')

    def test_order(self):
        first = self.first
        second = self.second
        third = self.third
        self.assertSequenceEqual(
            Todo.objects.values_list('pk'),
            [(first.pk,), (second.pk,), (third.pk,)]
        )

        # Reorder
        first.below(second)

        self.assertSequenceEqual(
            Todo.objects.values_list('pk'),
            [(second.pk,), (first.pk,), (third.pk,)]
        )

    def test_arbitrary_order(self):
        first = self.first
        second = self.second
        third = self.third
        self.assertSequenceEqual(
            Todo.objects.values_list('pk'),
            [(first.pk,), (second.pk,), (third.pk,)]
        )

        # Reorder
        first.to(1)

        self.assertSequenceEqual(
            Todo.objects.values_list('pk'),
            [(second.pk,), (first.pk,), (third.pk,)]
        )

    def test_ordered_render(self):
        c = Client()
        response = c.get('/')
        content = response.content

        # Test initial order
        first_index = content.find(self.first.description)
        second_index = content.find(self.second.description)
        third_index = content.find(self.third.description)
        self.assertLess(first_index, second_index)
        self.assertLess(second_index, third_index)

        # Reorder
        self.first.below(self.second)

        # Test reorder
        response = c.get('/')
        content = response.content

        first_index = content.find(self.first.description)
        second_index = content.find(self.second.description)
        third_index = content.find(self.third.description)
        self.assertLess(second_index, first_index)
        self.assertLess(first_index, third_index)


class TestOrderTaskViewTestCase(TransactionTestCase):
    def setUp(self):
        self.first = Todo.objects.create(description='first!')
        self.second = Todo.objects.create(description='second')
        self.third = Todo.objects.create(description='third')

    def test_reorder_view(self):
        first = self.first
        second = self.second
        third = self.third

        c = Client()
        response = c.post('/reorder/', {
            'id': first.id,
            'new_index': 2
        })
        self.assertEqual(response.status_code, 200)

        self.assertSequenceEqual(
            Todo.objects.values_list('pk', 'order'),
            [(second.pk, 0), (third.pk, 1), (first.pk, 2)]
        )
