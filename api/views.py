from ast import Pass
from base64 import urlsafe_b64encode
from datetime import datetime, timedelta
from django.conf import settings
from django.http import Http404, QueryDict
from django.shortcuts import get_object_or_404, render
import requests
from rest_framework.views import APIView
from api import serializers
from api import jwt_reset
from api.jwt_reset import JWTReset
from api.serializers import CreateUserSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
import jwt

User=get_user_model()
jwt_reset=JWTReset()

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
        
        if not user:
            print("Not User")
            raise Http404
        print(user.email)
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



class GetResetPasswordURLView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request,*args,**kwargs):
        # uid=urlsafe_base64_encode(force_bytes(request.user.pk))
        token=jwt_reset.encode_reset_token(user_id=request.user.pk)
        print(token)
        print(jwt_reset.decode_reset_token(reset_token=token))
        return Response(status=200)
        # subject=f'Password recovery for {request.user.email}'
    



