from django.test import TestCase
from django.contrib.auth.models import User
from task_manager.users.views import MyRegisterFormView


class CrudUserTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='PetrovF666',
            first_name='Fedor',
            last_name='Petrov',
        )
        user.set_password('qwerty88!')
        user.save()

    def test_user_login(self):
        true_login = self.client.login(username='PetrovF666', password='qwerty88!')
        false_login = self.client.login(username='PetrovF666', password='qwerty8888!')
        self.assertTrue(true_login, 'Correct login failed')
        self.assertFalse(false_login, 'Wrong login success')

    def test_user_create(self):
        form_data = {
            'username': 'ivanXXX',
            'first_name': 'ivan',
            'last_name': 'ivanov',
            'password1': 'passWORD1@',
            'password2': 'passWORD1@'
        }
        form = MyRegisterFormView(data=form_data)
        self.assertTrue(form.is_valid())

        self.client.post('/users/create/', form_data)
        self.assertTrue(User.objects.get(username='ivanXXX'))

    def test_user_update(self):
        form_data = {
            'username': 'PetrovF666',
            'first_name': 'Fedia',
            'last_name': 'Petrov',
        }
        user_id = User.objects.get(username='PetrovF666').id
        self.client.login(username='PetrovF666', password='qwerty88!')
        self.client.post(f'/users/{user_id}/update/', form_data)
        user = User.objects.get(username='PetrovF666')
        self.assertEqual(user.first_name, 'Fedia')

    def test_user_delete(self):
        user_id = User.objects.get(username='PetrovF666').id
        self.client.login(username='PetrovF666', password='qwerty88!')
        self.client.post(f'/users/{user_id}/delete/')
        self.assertFalse(User.objects.all())
