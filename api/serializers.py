from dataclasses import field
from pkg_resources import require
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
    email=serializers.EmailField()
    password=serializers.CharField(required=False)
    fullname=serializers.CharField(required=False)


    class Meta:
        model=User
        fields=['email','fullname','image','password']


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

        return data

