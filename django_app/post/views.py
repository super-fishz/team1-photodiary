from django.http import Http404
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from .models import Photo, Post
from .serializers import PhotoSerializer, PostSerializer
from rest_framework.response import Response


class PostList(generics.ListCreateAPIView):
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
    get요청시 해당 검색어의 제목검색 후
    포함 되는 제목의 글을 딕셔너리 형식(id : 글제목)으로 반환합니다.
    그 후 검색어와 제목을 비교해서
    해당글만 가져옵니다.
    '''
    def get(self, request):
        search_word = list(request.query_params.values())[0]
        all_queryset = self.request.user.post_set.all()
        all_post_list = list(all_queryset.values())
        title_id_dict = {}
        for number in range(0, len(all_post_list)):
            pop_title = all_post_list[number].pop('title')
            pop_post_id = all_post_list[number].pop('id')
            title_id_dict[pop_post_id] = pop_title
        search_result = []
        for key, value in title_id_dict.items():
            if search_word in str(value):
                post = Post.objects.get(pk=key)
                serializer = PostSerializer(post)
                search_result.append(serializer.data)
        return Response(search_result)


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
