from django.http import Http404, QueryDict
from django.shortcuts import get_object_or_404, render
import requests
from rest_framework.views import APIView
from api import serializers
from api.serializers import CreateUserSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.contrib.auth import get_user_model


User=get_user_model()

# Create your views here.


class CreateUserView(APIView):
    def post(self,request):
    
        data=request.data
        print(data)
        serializer=CreateUserSerializer(data=data)
        if not serializer.is_valid():
            
            return Response(status=400)
        else:
            data=serializer.save()
            return Response(data=data,status=200)


class TokenGetView(APIView):
    def post(self,request):
        data=request.data
        email=data['email']
        password=data['password']
        print(email)
        user=authenticate(username=email,password=password)
        if user:

            token=Token.objects.get(user=user)
            return Response({'token':token.key})

        else :
            return Response({"Invalid Login"})



class LoginUserView(APIView):
    def post(self,request):
        data=request.data
        print(data)
   
        
        user=authenticate(username=data['email'],password=data['password'])
        print(user.email)
        if not user:
            print("Not User")
            raise Http404
        serializer=UserSerializer(user,data=data)
        serializer.is_valid(raise_exception=True)
        print("User")
        token=get_object_or_404(Token,user=user)
        return Response({'token':token.key})

        



class UpdateProfilePictureView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    parser_classes=[MultiPartParser,FormParser]
    def post(self,request):
        picture=request.FILES['profile_pic']
        user=request.user
        user.profile_picture=picture
        print(str(user.profile_picture.url))
        user.save()
        return Response({'picture':user.profile_picture.url})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_data(request):
    
    user=request.user
    serializer=UserSerializer(user,context={'request':request})

    data=serializer.data


    del data['password']

    return Response(data)