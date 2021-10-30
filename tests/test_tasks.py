from django.test import TestCase
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
from task_manager.tasks.views import TaskCreationForm


class CrudTaskTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        Status.objects.create(name='created')
        Status.objects.create(name='updated')
        Status.objects.create(name='completed')

        user = User.objects.create_user(
            username='PetrovF666',
            first_name='Fedor',
            last_name='Petrov',
        )
        user.set_password('qwerty88!')
        user.save()
        user = User.objects.create_user(
            username='Petrov2',
            first_name='Fedor2',
            last_name='Petrov2',
        )
        user.set_password('qwerty88!')
        user.save()

        Task.objects.create(
            name='default_task',
            description='some task',
            status=Status.objects.get(name='completed'),
            author=User.objects.get(username='Petrov2'),
            executor=User.objects.get(username='PetrovF666')
        )

    def test_task_create(self):
        self.client.login(username='PetrovF666', password='qwerty88!')
        status = Status.objects.get(name='created')
        executor = User.objects.get(username='Petrov2')
        form_data = {
            'name': 'simple_task',
            'description': 'do something',
            'status': status.id,
            'executor': executor.id
        }
        form = TaskCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), 'Invalid form')

        self.client.post('/tasks/create/', form_data)
        task = Task.objects.get(name='simple_task')
        self.assertEqual(task.name, 'simple_task')
        self.assertEqual(task.author, User.objects.get(username='PetrovF666'))
        self.assertEqual(task.status, status)
        self.assertEqual(task.executor, executor)

    def test_task_update(self):
        self.client.login(username='PetrovF666', password='qwerty88!')
        status = Status.objects.get(name='updated')
        executor = User.objects.get(username='Petrov2')
        form_data = {
            'name': 'another simple_task',
            'description': 'do something else',
            'status': status.id,
            'executor': executor.id
        }
        task_id = Task.objects.get(name='default_task').id
        self.client.post(f'/tasks/{task_id}/update/', form_data)
        task = Task.objects.get(id=task_id)
        self.assertEqual(task.name, 'another simple_task')
        self.assertEqual(task.description, 'do something else')
        self.assertEqual(task.status, status)

    def test_task_delete(self):
        self.client.login(username='PetrovF666', password='qwerty88!')
        task_id = Task.objects.get(name='default_task').id
        self.client.post(f'/tasks/{task_id}/delete/')
        self.assertFalse(Task.objects.all())
