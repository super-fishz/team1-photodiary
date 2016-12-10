from rest_framework.serializers import ModelSerializer, raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from .models import MyUser

__all__ = [
    'MyUserSerializer',
    ]


class MyUserSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password', 'date_joined', 'id')
        write_only_fields = ('password',)


    def update(self, instance, validated_data):
        print()
        serializer = MyUserSerializer(instance, data=validated_data)
        password = validated_data['password']
        instance.set_password(password)
        instance.save()
        return instance