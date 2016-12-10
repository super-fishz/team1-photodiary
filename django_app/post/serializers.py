from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Post, Photo
from versatileimagefield.serializers import VersatileImageFieldSerializer


class PhotoSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'), ('medium_square_crop', 'crop__400x400'),
        ]
    )
    photo_id = serializers.SerializerMethodField()
    post_id = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ('image', 'post_id', 'photo_id')

    def get_photo_id(self, obj):
        return obj.pk

    def get_post_id(self, obj):
        return obj.post.pk

class PostSerializer(ModelSerializer):

    photos = PhotoSerializer(many=True, source='photo_set', read_only=True)
    author = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = '__all__'


    def get_author(self, obj):
        return obj.author.username
