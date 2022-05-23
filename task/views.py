from django.shortcuts import get_object_or_404, render
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import TaskSerializer
from .models import Task
from rest_framework.response import Response
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


class TaskDoneView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated] 
    def post(self,request):
        data=request.data
        stash={}
        if data:
            for value in data.values():
                task=get_object_or_404(Task,pk=value)
                task.is_done=True
                stash[str(value)]=task.is_done
                task.save()
            return Response(stash,status=200)
        else:
            return Response(status=400)




