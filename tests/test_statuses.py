from django.test import TestCase
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
from task_manager.statuses.views import StatusCreationForm


class CrudStatusTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Status.objects.create(name='Ultimate_status')
        user = User.objects.create_user(
            username='PetrovF666',
            first_name='Fedor',
            last_name='Petrov',
        )
        user.set_password('qwerty88!')
        user.save()

    def test_status_create(self):
        self.client.login(username='PetrovF666', password='qwerty88!')
        form_data = {
            'name': 'simple_status',
        }
        form = StatusCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), 'Invalid form')

        self.client.post('/statuses/create/', form_data)
        self.assertTrue(Status.objects.get(name='simple_status'))

    def test_status_update(self):
        self.client.login(username='PetrovF666', password='qwerty88!')
        form_data = {
            'name': 'simple_status',
        }
        status_id = Status.objects.get(name='Ultimate_status').id
        self.client.post(f'/statuses/{status_id}/update/', form_data)
        status = Status.objects.get(id=status_id)
        self.assertEqual(status.name, 'simple_status')

    def test_user_delete(self):
        self.client.login(username='PetrovF666', password='qwerty88!')
        status_id = Status.objects.get(name='Ultimate_status').id
        self.client.post(f'/statuses/{status_id}/delete/')
        self.assertFalse(Status.objects.all())
