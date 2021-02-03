from django.core.management import call_command
from django.test import TestCase, Client

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


class TestAuthUserCase(TestCase):

    def setUp(self):
        call_command('flush', '--noinput')
        self.client = Client()

        self.superuser = ShopUser.objects.create_superuser('django', 'django@gd.local', 'geekbrains')

        self.user = ShopUser.objects.create_user('test1', 'test1@gd.local', 'geekbrains')
        self.user_with_fn = ShopUser.objects.create_user('test2', 'test2@gd.local', 'geekbrains', first_name='Test2')

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertNotContains(response, 'Пользователь', status_code=200)

        self.client.login(username='django', password='geekbrains')

        response = self.client.get('/authapp/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.superuser)
        # self.assertContains(response, 'Пользователь', status_code=200)

    def test_user_logout(self):
        self.client.login(username='django', password='geekbrains')

        response = self.client.get('/authapp/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)


        response = self.client.get('/authapp/logout/')
        self.assertEqual(response.status_code, 302)

    def test_basket_user_login_redirect(self):
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'auth/login/?next=/basket/')

        self.client.login(username='django', password='geekbrains')
        #
        #
        # response = self.client.get('/authapp/login/')
        #
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/basket/')

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')
