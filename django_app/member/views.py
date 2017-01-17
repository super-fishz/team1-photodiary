from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import AuthTokenSerializer
from member.models import MyUser
from member.serializers import MyUserSerializer


class CreateUser(generics.ListCreateAPIView):
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()

    def create(self, request, *args, **kwargs):
        '''
        회원가입
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        result = dict(serializer.data)
        result.pop('password')
        return Response(result, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        '''
        모든 회원 리스트
        '''
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        results = []
        for test in serializer.data:
            result = dict(test)
            result.pop('password')
            results.append(result)
        return Response(results)


class DetailUser(generics.UpdateAPIView, APIView):
    serializer_class = MyUserSerializer

    def get(self, request):
        '''
        유저 디테일
        '''
        instance = MyUser.objects.get(email=request.user.email)
        serializer = self.serializer_class(instance)
        result = dict(serializer.data)
        result.pop('password')
        return Response(result)

    def update(self, request, *args, **kargs):
        '''
        패스워드 변경
        '''
        instance = MyUser.objects.get(email=request.user.email)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        result = dict(serializer.data)
        result.pop('password')
        return Response("비밀번호가 변경 되었습니다.")


class Login_ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = AuthTokenSerializer

    def post(self, request):
        '''
        로그인
        '''
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class Logout_RemoveAuthToken(APIView):
    queryset = MyUser.objects.all()
    def get(self, request):
        '''
        로그아웃
        '''
        Token.objects.get(user=request.user).delete()
        return Response("로그아웃 완료되었습니다.", status=status.HTTP_200_OK)
