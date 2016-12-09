from rest_framework.serializers import ModelSerializer
from .models import MyUser

__all__ = [
    'MyUserSerializer',
    ]


class MyUserSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password', 'date_joined', 'id')
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
