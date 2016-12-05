from rest_framework.serializers import ModelSerializer
from .models import Post, Photo



class Postserializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'author', 'content',
                  'modified_date', 'created_date')


class Photoserializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = ('author',
                  'modified_date', 'created_date', 'image', 'post')