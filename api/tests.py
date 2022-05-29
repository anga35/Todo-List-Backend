from distutils.command.upload import upload
from http import client
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.conf import settings
User=get_user_model()
# Create your tests here.
class TestEndpoints(TestCase):


    def setUp(self) -> None:
        data={'email':'test@gmail.com',
        'password':'test12345',
        'password1':'test12345',
        'fullname':'Test David'}
        response=self.client.post(reverse('create-user'),data=data)
        self.user=User.objects.get(email='test@gmail.com')
        self.token=Token.objects.get(user=self.user)
        print(response)

    def test_create_user(self):
        data={'email':'dayodele89@gmail.com',
        'password':'david12345',
        'password1':'david12345',
        'fullname':'Ayodele David'}
        print(reverse('create-user'))
        response=self.client.post(reverse('create-user'),data=data,content_type='application/json')
        print(response.json())

    def test_login_user(self):
        data={'email':'test@gmail.com',
        'password':'test12345'
       }
        response=self.client.post(reverse('login-user'),data=data)
        return response.json()

    def test_get_user_data(self):
        
        token=self.test_login_user()['token']
        auth_header=f'Token {token}'
        response=self.client.get(reverse('get-user'),HTTP_AUTHORIZATION=auth_header)
        print(response.json())

    def test_profile_pic(self):
        pic_dir=getattr(settings,'MY_IMG',None)
        picture=open(pic_dir,'rb')
        upload={'profile_pic':picture}
        response=self.client.post(reverse('profile-pic'),data=upload,HTTP_AUTHORIZATION=f'Token {self.token.key}')
        print(response.json())


