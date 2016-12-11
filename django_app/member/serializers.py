from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import MyUser
from django.utils.translation import ugettext_lazy as _


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('username', 'id', 'password', 'email', 'date_joined')

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user = MyUser.objects.create(
          username=username,
          email=email
        )
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data['password']
        user = instance
        user.set_password(password)
        user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("email"))
    password = serializers.CharField(label=_("password"), style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    msg = _('유저의 활동이 정지되었습니다.')
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = _('해당 유저의 로그인 정보가 없습니다.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('email과 password를 입력해야 합니다.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs