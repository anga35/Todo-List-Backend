from django.test import TestCase
from django.contrib.auth import get_user_model

User=get_user_model()
# Create your tests here.
class UserTest(TestCase):


#Create base user test
    def test_createuser(self):

        user=User.objects.create_user(email='david@gmail.com',password='david123bcd',fullname="Ayodele David")

        self.assertEqual(user.fullname,'Ayodele David')



#Create staff user test
    def test_create_staffuser(self):
        user=User.objects.create_staffuser(email='david@gmail.com',password='david123bcd',fullname="Ayodele David")
        self.assertEqual(user.fullname,'Ayodele David')
        self.assertTrue(user.is_staff)

#Create super user tests
    def test_create_superuser(self):
        user=User.objects.create_superuser(email='david@gmail.com',password='david123bcd',fullname="Ayodele David")
        self.assertEqual(user.fullname,'Ayodele David')
        self.assertTrue(user.is_superuser)
    