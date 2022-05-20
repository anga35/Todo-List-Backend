from django.test import TestCase
from django.urls import reverse
# Create your tests here.
class TestEndpoints(TestCase):

    def test_create_user(self):
        data={'email':'dayodele89@gmail.com',
        'password':'david12345',
        'password1':'david12345',
        'fullname':'Ayodele David'}
        print(reverse('create-user'))
        response=self.client.post(reverse('create-user'),data)
        print(response)

