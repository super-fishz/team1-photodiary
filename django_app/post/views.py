from django.http import Http404
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from .models import Photo, Post
from .serializers import PhotoSerializer, PostSerializer
from rest_framework.response import Response


class PostList(generics.ListCreateAPIView, APIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return self.request.user.post_set.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)
        for file in request.FILES.getlist('image'):
            Photo.objects.create(post=post, image=file)
        return Response(serializer.data)


from .permision import Isthatyours
class PostDetail(APIView):
    permission_classes = (Isthatyours,)

    def get_object(self, pk):

        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        origin_serializer = PostSerializer(post)
        origin_title = origin_serializer.data['title']
        modify_serializer = PostSerializer(post, data=request.data)
        if modify_serializer.is_valid():
            modify_serializer.save()
            return Response(modify_serializer.data)
        elif 'title' not in request.data:
            request.data['title'] = origin_title
            modify_serializer = PostSerializer(post, data=request.data)
            if modify_serializer.is_valid():
                modify_serializer.save()
                return Response(modify_serializer.data)
        else:
            return Response(modify_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Post_title_search(APIView):
    '''
    get요청시 해당 검색어의 제목검색
    '''
    def get(self, request):
        search_list = []
        # for title in self.request.user.post_set.all():
        #     search_list.append(title)
        #     print (search_list)

        print('-' * 29)
        all_queryset = self.request.user.post_set.all()
        all_post_list = list(all_queryset.values())
        print(len(all_post_list))
        pop_title = all_post_list[0].pop('title')
        pop_post_id = all_post_list[0].pop('id')
        print(pop_title)
        print(pop_post_id)

        print('-' * 29)


class PhotoList(generics.ListCreateAPIView):
    serializer_class = PhotoSerializer
    queryset = {'post', 'image'}


class PhotoDetail(APIView):

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        photo = self.get_object(pk)
        serializer = PhotoSerializer(photo)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        photo = self.get_object(pk)
        serializer = PhotoSerializer(photo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        photo = self.get_object(pk)
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
