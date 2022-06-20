
from base64 import urlsafe_b64encode

from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
import requests
from rest_framework.views import APIView

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
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template import loader
from django.core.mail import EmailMultiAlternatives

from account.custom_password_reset import CustomPasswordReset

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

    def generate_url(self,uid,token):
        return reverse('get-reset-password-url',kwargs={'uidb64':uid,'token':token})

    def get(self,request,*args,**kwargs):

        user=request.user
        password_reset=CustomPasswordReset()
        token=password_reset.make_token(user)
        uid=urlsafe_base64_encode(force_bytes(request.user.pk))
        email_template_html=loader.render_to_string('api/email_reset.html',context={'token':token,'uid':uid})
        print(email_template_html)
        subject="Password Reset"
        email_from=settings.EMAIL_HOST_USER
        recipient_list=[user.email]
        email_message=EmailMultiAlternatives(subject,email_template_html,email_from,recipient_list)
        email_message.attach_alternative(email_template_html,'text/html')
        email_message.send()
        return Response(status=200)
        # subject=f'Password recovery for {request.user.email}'





class ResetPassword(View):

    def get(self,request,*args,**kwargs):
        uid=kwargs['uidb64']
        token=kwargs['token']


        pk=urlsafe_base64_decode(uid).decode()
        user=User.objects.get(pk=pk)
        is_token_valid=CustomPasswordReset().check_token(user,token)

        print(pk)
        print(is_token_valid)

        return render(request,'api/password_reset.html')

    def post(self,request,*args,**kwargs):
        uid=kwargs['uidb64']
        uid=urlsafe_base64_decode(uid).decode()
        data=request.POST
        
        password=data['password']
        password1=data['password1']

        if(password!=password1):
            return render(request,'api/password_reset.html',{'wrong_password':True})

        user=User.objects.get(pk=uid)
        user.set_password(password)
        user.save()
        

        return redirect(reverse('reset-complete'))
    
    

def reset_complete(request):

    return render(request,'api/reset_complete.html')

