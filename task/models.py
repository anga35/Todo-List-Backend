from django.db import models
from django.contrib.auth import get_user_model


User=get_user_model()
# Create your models here.
class Task(models.Model):
    name=models.CharField(max_length=100)
    user=models.ForeignKey(User,related_name='tasks',related_query_name='task',on_delete=models.SET_NULL,null=True,blank=True)
    create_date=models.DateTimeField(auto_now_add=True)
    deadline=models.DateTimeField(null=True,blank=True)
    is_done=models.BooleanField(default=False)
