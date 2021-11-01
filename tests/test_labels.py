from django.test import TestCase
from task_manager.labels.models import Label
from django.contrib.auth.models import User
from task_manager.labels.views import LabelCreationForm


class CrudStatusTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Label.objects.create(name='Ultimate_label')
        user = User.objects.create_user(
            username='PetrovF666',
            first_name='Fedor',
            last_name='Petrov',
        )
        user.set_password('qwerty88!')
        user.save()

    def test_label_create(self):
        self.client.login(username='PetrovF666', password='qwerty88!')
        form_data = {
            'name': 'simple_label',
        }
        form = LabelCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), 'Invalid form')

        self.client.post('/labels/create/', form_data)
        self.assertTrue(Label.objects.get(name='simple_label'))

    def test_label_update(self):
        self.client.login(username='PetrovF666', password='qwerty88!')
        form_data = {
            'name': 'simple_label',
        }
        label_id = Label.objects.get(name='Ultimate_label').id
        self.client.post(f'/labels/{label_id}/update/', form_data)
        label = Label.objects.get(id=label_id)
        self.assertEqual(label.name, 'simple_label')

    def test_label_delete(self):
        self.client.login(username='PetrovF666', password='qwerty88!')
        label_id = Label.objects.get(name='Ultimate_label').id
        self.client.post(f'/labels/{label_id}/delete/')
        self.assertFalse(Label.objects.all())
