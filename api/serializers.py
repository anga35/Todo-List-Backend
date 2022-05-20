from dataclasses import field
from rest_framework.authtoken.models import Token
from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model


User=get_user_model()


class TokenSerializer(serializers.ModelSerializer):



    class Meta:
        model=Token
        fields=['key']



class UserSerializer(serializers.ModelSerializer):
    class meta:
        model=User
        fields=['email,fullname,image']


class CreateUserSerializer(serializers.ModelSerializer):

    
    password1=serializers.CharField(required=True)

    class Meta:
        model=User
        fields=['email','fullname','image','password','password1']


    def validate(self, attrs):

        if( attrs['password']!= attrs['password1']):
            raise ValidationError("Passwords not corresponding")


        return super().validate(attrs)


    def save(self, **kwargs):
        data=self.validated_data


        email=data['email']
        password=data['password']
        password1=data['password1']
        fullname=data['fullname']
   


        

        user=User.objects.create_user(email=email,password=password,fullname=fullname)


        token=Token.objects.get_or_create(user=user)
        
       
        data['token']=token[0].key

        return data

