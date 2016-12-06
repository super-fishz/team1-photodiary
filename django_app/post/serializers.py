from rest_framework.serializers import ModelSerializer
from .models import Post, Photo
from versatileimagefield.serializers import VersatileImageFieldSerializer


class PhotoSerializer(ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'), ('medium_square_crop', 'crop__400x400'),
        ]
    )

    class Meta:
        model = Photo
        # fields = ('image', 'modified_date', 'created_date', 'image')
        fields = '__all__'


class PostSerializer(ModelSerializer):

    photos = PhotoSerializer(many=True, source='photo_set', read_only=True)

    class Meta:
        model = Post
        # fields = ('title', 'author', 'content', 'modified_date', 'created_date', 'photos')
        fields = '__all__'
