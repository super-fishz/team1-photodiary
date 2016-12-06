from rest_framework.serializers import ModelSerializer, ImageField
from .models import Post, Photo
from versatileimagefield.serializers import VersatileImageFieldSerializer

class Photoserializer(ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('medium_square_crop', 'crop__400x400'),
        ]
    )
    class Meta:
        model = Photo
        fields = ('image',
                  'modified_date', 'created_date', 'image')


class Postserializer(ModelSerializer):

    photos = Photoserializer(many=True, source='photo_set', read_only=True)

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


