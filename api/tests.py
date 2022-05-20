from django.test import TestCase
from django.urls import reverse
# Create your tests here.
class TestEndpoints(TestCase):


    def setUp(self) -> None:
        data={'email':'test@gmail.com',
        'password':'test12345',
        'password1':'test12345',
        'fullname':'Test David'}
        response=self.client.post(reverse('create-user'),data=data)
        print(response)

    def test_create_user(self):
        data={'email':'dayodele89@gmail.com',
        'password':'david12345',
        'password1':'david12345',
        'fullname':'Ayodele David'}
        print(reverse('create-user'))
        response=self.client.post(reverse('create-user'),data)
        print(response)

    def test_login_user(self):
        data={'email':'test@gmail.com',
        'password':'test12345'
       }
        response=self.client.post(reverse('login-user'),data=data)
        print(response.json())

