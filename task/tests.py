import email
import imp
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
        print(response)


    def test_createTask(self):
        user=User.objects.get(email='test@gmail.com')
        task=Task.objects.create(name="Do this",user=user)
        print(task.is_done)
        task_name=user.tasks.all().first().name
        self.assertEqual(task_name,'Do this')
