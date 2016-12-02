
from django.contrib.auth import authenticate, get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers, exceptions
from rest_auth.serializers import LoginSerializer
from .models import MyUser


class MyUserserializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password', 'date_joined', 'pk')
        write_only_fields = ('password',)


    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user = MyUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return user
