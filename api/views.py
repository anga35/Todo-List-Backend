from django.http import Http404
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from api import serializers
from api.serializers import CreateUserSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser,FormParser
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

        



class UpdateProfilePictureView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    parser_classes=[MultiPartParser,FormParser]
    def post(self,request):
        picture=request.data['profile_pic']
        user=request.user
        user.profile_picture=picture
        print(user.profile_picture.url)
        return Response("Done")