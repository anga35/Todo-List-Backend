import email
import imp
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.urls import reverse
from .models import Task
from django.contrib.auth import get_user_model

User=get_user_model()

# Create your tests here.
class TaskTest(TestCase):

    def setUp(self):
        data={'email':'test@gmail.com',
        'password':'test12345',
        'password1':'test12345',
        'fullname':'Test David'}
        response=self.client.post(reverse('create-user'),data=data)
        self.user=User.objects.get(email='test@gmail.com')
        self.token=Token.objects.get(user=self.user)
        


    def test_createTask(self):
        user=User.objects.get(email='test@gmail.com')
        task=Task.objects.create(name="Do this",user=user)
        task_name=user.tasks.all().first().name
        self.assertEqual(task_name,'Do this')

    def test_get(self):
     
        task=Task.objects.create(name="Do this",user=self.user)
        response=self.client.get(reverse('task-all'),HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response_name=response.json()[0]['name']
        self.assertEqual(response_name,'Do this')

    def test_create(self):
        data={'name':'Jump out the house'}
        response=self.client.post(reverse('task-create'),HTTP_AUTHORIZATION=f'Token {self.token.key}',data=data)
        print(self.user.tasks.all())
        print(response.json())