from rest_framework.serializers import ModelSerializer, ImageField
from .models import Post, Photo

class Photoserializer(ModelSerializer):

    class Meta:
        model = Photo
        fields = ('image',
                  'modified_date', 'created_date')


class Postserializer(ModelSerializer):

    photos = Photoserializer(many=True, source='photo_set')

    class Meta:
        model = Post
        fields = ('title', 'author', 'content',
                  'modified_date', 'created_date', 'photos')


    # def create(self, validated_data):
    #     print(validated_data)
    #     photos_data = validated_data.pop('images')
    #     post = Post.objects.create(**validated_data)
    #     print('ddddddddddd')
    #     print(post)
    #     print(photos_data)
    #     for photo_data in photos_data:
    #         Photo.objects.create(post=post, **photo_data)
    #     return post


