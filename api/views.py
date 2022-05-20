from django.http import Http404
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from api import serializers
from api.serializers import CreateUserSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
# Create your views here.


class CreateUserView(APIView):
    def post(self,request):
        data=request.data
        serializer=CreateUserSerializer(data=data)

        if not serializer.is_valid():
            return Response(status=400)


        else:
            data=serializer.save()
            return Response(data=data,status=200)


class LoginUserView(APIView):


    def post(self,request):
        data=request.data
        user=authenticate(username=data['email'],password=data['password'])

        if not user:
            raise Http404
        serializer=UserSerializer(user,data=data)

        serializer.is_valid(raise_exception=True)
        token=get_object_or_404(Token,user=user)
        return Response({'token':token.key})



            