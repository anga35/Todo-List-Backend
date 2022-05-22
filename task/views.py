from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import TaskSerializer
# Create your views here.
class TaskListView(ListCreateAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class=TaskSerializer



    def get_queryset(self):
        user=self.request.user
        return user.tasks.all()


    def perform_create(self, serializer):
        user=self.request.user


        serializer.save(user=user)





