import io
import random
import urllib.request
import zipfile
from datetime import timedelta

import boto
from boto.s3.key import Key
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import Http404
from django.utils import timezone
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Photo, Post, TodayPhoto, Today3photo, SelectTodayPhoto
from .serializers import PostSerializer, TodayPhotoSerializer, Today3photoSerializer
from .permission import Isthatyours


class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        '''
        유저정보를 이용해 해당 유저의 글 목록을 보여주기 위한 오버라이딩이다.
        list()함수내에 페이지네이션이 들어가 있으므로 자동으로 페이지 네이션이 됬다.
        '''
        queryset = self.request.user.post_set.all().order_by('-created_date')
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)

        for file in request.data.getlist('image'):
            Photo.objects.create(post=post, image=file)
        return Response(serializer.data)


class PostDetail(APIView):
    permission_classes = (Isthatyours,)

    def get_object(self, post_pk):
        try:
            return Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, post_pk, format=None):
        post = self.get_object(post_pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, post_pk, format=None):
        post = self.get_object(post_pk)
        origin_serializer = PostSerializer(post)
        origin_title = origin_serializer.data['title']
        modify_serializer = PostSerializer(post, data=request.data)

        if modify_serializer.is_valid():
            for file in request.FILES.getlist('image'):
                Photo.objects.create(post=post, image=file)
            modify_serializer.save()
            return Response(modify_serializer.data)
        elif 'title' not in request.data:
            for file in request.FILES.getlist('image'):
                Photo.objects.create(post=post, image=file)
            request.data['title'] = origin_title
            modify_serializer = PostSerializer(post, data=request.data)
            if modify_serializer.is_valid():
                modify_serializer.save()
                return Response(modify_serializer.data)
        else:
            return Response(modify_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_pk, format=None):
        post = self.get_object(post_pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class PostTitleSearch(APIView):
#     '''
#     get요청시 해당 검색어의 제목검색 후
#     포함 되는 제목의 글을 딕셔너리 형식(id : 글제목)으로 반환합니다.
#     그 후 검색어와 제목을 비교해서
#     해당글만 가져옵니다.
#     '''
#     def get(self, request):
#         search_word = list(request.query_params.values())[0]
#         all_queryset = self.request.user.post_set.all()
#         all_post_list = list(all_queryset.values())
#         title_id_dict = {}
#         for number in range(0, len(all_post_list)):
#             pop_title = all_post_list[number].pop('title')
#             pop_post_id = all_post_list[number].pop('id')
#             title_id_dict[pop_post_id] = pop_title
#         search_result = []
#         for key, value in title_id_dict.items():
#             if search_word in str(value):
#                 post = Post.objects.get(pk=key)
#                 serializer = PostSerializer(post)
#                 search_result.append(serializer.data)
#         return Response(search_result)

class PostTitleSearch(generics.ListAPIView):
    """
    글 검색 기능, list()함수 내에서 실행되는 get_queryset함수를 오버라이딩하니
    3줄만에 기능 구현이 됬다.

    self.request.user.post_set.filter
    500에러남
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        search_word = self.request.query_params['title']
        queryset = self.request.user.post_set.filter(title__contains=search_word)
        return queryset



class PhotoDetail(APIView):
    permission_classes = (Isthatyours,)

    def get_post_object(self, post_pk):
        try:
            return Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, post_pk, format=None):
        post = self.get_post_object(post_pk)
        post_serializer = PostSerializer(post)
        post_photo_list = post_serializer.data['photos']
        return Response(post_photo_list)

    def put(self, request, post_pk, format=None):
        return Response('this url is not allowed "PUT" method')

    def delete(self, request, post_pk, photo_pk, format=None):
        post = self.get_post_object(post_pk)
        if photo_pk:
            photos = post.photo_set.get(pk=photo_pk)
            photos.delete()
        else:
            photos = post_pk.photo_set.all()
            photos.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateTodayPhoto(generics.CreateAPIView):
    serializer_class = TodayPhotoSerializer
    queryset = TodayPhoto

    def create(self, request, *args, **kwargs):
        """
        오늘의 사진 올리기
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author='superuser')
        return Response(serializer.data)


class PickTodayPhoto(APIView):
    queryset = TodayPhoto

    def new3photo(self):
        '''
        Todayphoto 의 3가지 종류의 사진들중 하나씩을 랜덤으로 뽑아 Today3photo 객체를
        만들어 리턴하는 함수입니다.
        '''
        good_count = TodayPhoto.objects.filter(is_good=True).count()
        bad_count = TodayPhoto.objects.filter(is_bad=True).count()
        know_count = TodayPhoto.objects.filter(is_not_know=True).count()
        index1 = random.randint(0, good_count - 1)
        index2 = random.randint(0, bad_count - 1)
        index3 = random.randint(0, know_count - 1)
        good_photo = TodayPhoto.objects.filter(is_good=True)[index1]
        bad_photo = TodayPhoto.objects.filter(is_bad=True)[index2]
        know_photo = TodayPhoto.objects.filter(is_not_know=True)[index3]

        return Today3photo.objects.create(photo1=good_photo, photo2=bad_photo, photo3=know_photo)

    def get(self, request):
        '''
        만약 Today3photo 오브젝트가 하나도 없으면 바로 생성합니다.
        오브젝트가 있고 그것이 생성한지 하루가 지나지 않았으면 마지막 오브젝트를 리턴합니다
        하루가 지났다면 다시 생성하고 그것을 리턴합니다.
        '''
        if Today3photo.objects.exists():
            if timezone.now() - Today3photo.objects.last().created_date < timedelta(days=1):
                result = Today3photoSerializer(Today3photo.objects.last())

                return Response({
                    "오류메시지": "하루가 지나야 생성 가능합니다.",
                    "마지막으로 만든 데이터": result.data,
                    "photo1": Today3photo.objects.last().photo1.image.url,
                    "photo2": Today3photo.objects.last().photo2.image.url,
                    "photo3": Today3photo.objects.last().photo3.image.url
                    })
            else:
                result = Today3photoSerializer(self.new3photo())
                return Response(result.data)
        else:
            result = Today3photoSerializer(self.new3photo())
            return Response(result.data)


    def post(self, request, select_id):
        '''
        유저가 select_id 를 통해 3개의 사진 중 하나를 선택하면
        그 사진을 포함한 글을 작성 할 수 있습니다.
        글이 작성되고 Todayphoto 모델에 선택한 유저와, 선택한 유저의 카운터를 +1 시키고
        해당 글을 리턴합니다. 그리고 함께 3가지 사진들 중 유저들이 선택한 횟수의 비율도 함께 보여줍니다.

        유저가 select_id를 통해 사진을 하나 고를때 오늘의 사진에 있는 id값인지 검사를 먼저 합니다.
        '''

        if request.user.is_anonymous:
            raise Exception("토큰값을 주셔야 합니다.")
        else:
            # if select_id == list({k: Today3photo.objects.last().__dict__[k] for k
            #                       in ('photo1_id', 'photo2_id', 'photo3_id')}.values()):
            if int(select_id) in [value for key, value in Today3photo.objects.values().last().items() if 'photo' in key]:
                pass
            else:
                return Response("URL에 입력하신 아이디는 오늘의 사진에 없는 사진 ID입니다.")
            image = TodayPhoto.objects.get(pk=select_id)
            image.select_count += 1
            image.save()
            many = SelectTodayPhoto(user=request.user, photo=image)
            many.save()

            serializer = PostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            post = serializer.save(author=request.user)
            Photo.objects.create(post=post, image=image.image)
            self.request.user.post_set.all().order_by('-created_date')
            recently_3photo = Today3photo.objects.last()
            select_count = recently_3photo.photo1.select_count\
                + recently_3photo.photo2.select_count\
                + recently_3photo.photo3.select_count
            percentage = image.select_count / select_count * 100

            result = dict(serializer.data)
            result['percent'] = percentage

        return Response(result)


class ZipAndSendMail(APIView):

    def get(self, request):
        '''
        해당 url로 접속하면 해더에 있는
        토큰을 가진 유저의 마지막 사진부터 x개를 압축한다음
        S3에 업로드 한다.
        그후 업로드된 파일의 주소를 해당 유저의 이메일로 보내준다.
        '''
        image_list = []
        number = int(request.query_params['number'])
        for i in Photo.objects.filter(post__author=request.user.id).reverse()[:number]:
            image = "https://team1-photodiary.s3.amazonaws.com/media/{}".format(i.image)
            image_list.append(image)
        f = io.BytesIO()
        zip = zipfile.ZipFile(f, 'w')
        count = 0
        for url in image_list:
            count += 1
            url = urllib.request.urlopen(url)
            zip.writestr('{}.jpg'.format(count), url.read())
        zip.close()

        try:
            c = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
            b = c.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
            k = Key(b)
            k.key = 'zipfile/{}.zip'.format(request.user)
            k.set_contents_from_string(f.getvalue())
        except:
            raise Response("S3 업로드에 실패했습니다. 관리자에게 문의하세요 ", status=status.HTTP_504_GATEWAY_TIMEOUT)

        try:
            email = EmailMessage(
                '[사진다이어리]안녕하세요 요청하신대로 사진 {}개 압축파일로 만들었어요!'.format(number),
                '다운로드 받으실수 있는 주소는 https://team1-photodiary.s3.amazonaws.com/zipfile/{}.zip입니다.'.format(request.user),
                to=['lys0333@gmail.com'],
            )
            email.send()
        except Exception as e:
            raise APIException({"detail": e.args})
        return Response("압축 후 메일 보내기에 성공했습니다.", status=status.HTTP_200_OK)
