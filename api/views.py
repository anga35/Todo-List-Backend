from django.shortcuts import render
from rest_framework.views import APIView
from api.serializers import CreateUserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
# Create your views here.


class CreateUserView(APIView):


    def post(self,request):

        data=request.data

        serializer=CreateUserSerializer(data=data)

        if not serializer.is_valid():
            return Response(status=400)


        else:
            data=serializer.save()
            print(data)
            return Response(data=data,status=200)


            