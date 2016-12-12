from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Post, Photo, TodayPhoto
from versatileimagefield.serializers import VersatileImageFieldSerializer
import sys


class PhotoSerializer(serializers.ModelSerializer):
    # image = VersatileImageFieldSerializer(sizes='images')
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


class TodayPhotoSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'), ('medium_square_crop', 'crop__400x400'),
        ]
    )

    class Meta:
        model = TodayPhoto
        fields = '__all__'

    def create(self, validated_data):
        title = validated_data['title']
        image = validated_data['image']
        good = validated_data['is_good']
        bad = validated_data['is_bad']
        not_know = validated_data['is_not_know']
        if good or bad or not_know:
            todayphoto = TodayPhoto.objects.create(
                title=title,
                image=image,
                is_good=good,
                is_bad=bad,
                is_not_know=not_know
            )
            todayphoto.save()
            return todayphoto
        else:
            msg = "is_good, is_bad, is_now_know 중 하나는 True 여야 합니다."
            raise serializers.ValidationError(msg)


