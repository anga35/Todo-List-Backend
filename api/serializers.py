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
    profilePicture=serializers.CharField(allow_null=True,allow_blank=True,required=False)

    class Meta:
        model=User
        fields=['email','fullname','profilePicture','password','tasks']

    def get_profilePicture(self,obj):
        return obj.email


class CreateUserSerializer(serializers.ModelSerializer):   
    password1=serializers.CharField(required=True,write_only=True)

    class Meta:
        model=User
        fields=['email','fullname','profile_picture','password','password1']

    def validate(self, attrs):

        if( attrs['password']!= attrs['password1']):
            raise serializers.ValidationError("Wrong password")


        return super().validate(attrs)


    def save(self, **kwargs):
        data=self.validated_data
        email=data['email']
        password=data['password']
        password1=data['password1']
        fullname=data['fullname']
        user=User.objects.create_user(email=email,password=password,fullname=fullname)
        token=Token.objects.get_or_create(user=user)
        del data['password1']
        del data['password']
        if user.profile_picture:
            data['profile_picture']=user.profile_picture.url
        return data

