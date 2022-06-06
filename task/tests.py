import email
import imp
import json
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
        print(user.email)
        task=Task.objects.create(name="Do this",user=user)
        task_name=user.tasks.all().first().name
        self.task_pk=user.tasks.all().first().pk
        
        self.assertEqual(task_name,'Do this')

    def test_get(self):
        Task.objects.create(name="Do this",user=self.user)
        task=Task.objects.create(name="Do this",user=self.user)
        response=self.client.get(reverse('task-all'),HTTP_AUTHORIZATION=f'Token {self.token.key}')
        print(response.json())
        response_name=response.json()[0]['name']
        self.assertEqual(response_name,'Do this')

    def test_create(self):
        data=[{'name':'Jump out the house','deadline':'2022-05-26T20:45:45'},{'name':'Jump out tha house','deadline':'2022-05-26T20:45:45'}]
        response=self.client.post(reverse('task-create'),HTTP_AUTHORIZATION=f'Token {self.token.key}',data=data,content_type='application/json')
        print(self.user.tasks.all())
        print(response.json())


    def test_task_done(self):
        self.test_createTask()
        self.test_createTask()
        task_items={'pk':[1,2]}
        response=self.client.post(reverse('task-done'),HTTP_AUTHORIZATION=f'Token {self.token.key}',data=task_items,content_type='application/json')
        print(response.json())


    def test_null(self):
        data=[{'items':['a','b','v']}]
        response=self.client.post(reverse('testo'),data=data,content_type='application/json')
        print(response.json())

        
