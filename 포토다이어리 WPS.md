

## 유저 관련

### 회원가입, 유저 리스트

:  회원가입과 유저의 리스트를 볼 수 있습니다.

 <http://photodiary-dev.ap-northeast-2.elasticbeanstalk.com/member/user/>

- GET 요청시 유저 리스트를 반환합니다.

결과값 예시

~~~
[
  {
    "username": "team1",
    "email": "lys0333@gmail.com",
    "password": "pbkdf2_sha256$30000$GPsyRFilUgUw$ur3LAKSDNCLYJk7XuVJg6/HuUmYohEdCkdMZLSM2w0k=",
    "date_joined": "2016-12-02T08:35:47.334190Z",
    "pk": 1
  },
  {
    "username": "test",
    "email": "test@test.com",
    "password": "pbkdf2_sha256$30000$a6VeYhMvcDcR$eYz/0LcGCamfrdrpCorpbly+HENPA4O2VTS3TU5cU/Q=",
    "date_joined": "2016-12-02T10:20:04.625813Z",
    "pk": 2
  }
]
~~~
- POST 요청시 해당 유저를 만들고 해당 유저 정보를 보냅니다.


입력해야 하는 필드 키 이름
>username

>email

>password

결과값 예시
~~~
{
  "username": "test11",
  "email": "test11@test.com",
  "password": "pbkdf2_sha256$30000$OmIu4bCXpraz$KBj/ZzvWiLtLsmeXP1lKWaG6oHtd41+GKTnISzIvSRo=",
  "date_joined": "2016-12-02T10:31:00.892369Z",
  "pk": 4
}
~~~
---
### 로그인
: 로그인 후 해당 유저의 토큰을 반환합니다.

<http://photodiary-dev.ap-northeast-2.elasticbeanstalk.com/member/auth/login/>

- POST 요청시

입력해야하는 필드 키 이름
>email

>password

결과값 예시
```
{"key":"8d070f1a0f79e54738b0eec6bdb87455da18f011"}
```
## 글 관련
: 로그인한 해당 유저의 글 목록과 해당 글에 포함되어있는 사진의 url을 볼 수 있습니다.

<http://photodiary-dev.ap-northeast-2.elasticbeanstalk.com/post/>

---

***※※※아래 GET요청과 POST요청에는 꼭 해더에 로그인 할 때 받는 토큰값이 들어가야합니다.※※※***

***해더 필드 키 이름***
***key -> Authorization***
***value -> Token <로그인시 받는 해당 유저 토큰>***

---

- GET 요청시 해당 유저의 글 리스트들과 해당 글의 포토들이 반환됩니다.

결과값 예시

~~~
[
  {
    "title": "업로드 테스트****",
    "author": 2,
    "content": "업로드 테스트****",
    "modified_date": "2016-12-05T16:36:44.566548Z",
    "created_date": "2016-12-05T16:36:44.566581Z",
    "photos": [
      {
        "image": "https://team1-photodiary.s3.amazonaws.com/media/photo/photo/9.jpg",
        "modified_date": "2016-12-05T16:36:44.605183Z",
        "created_date": "2016-12-05T16:36:44.605217Z"
      },
      {
        "image": "https://team1-photodiary.s3.amazonaws.com/media/photo/photo/1.jpg",
        "modified_date": "2016-12-05T16:36:46.031145Z",
        "created_date": "2016-12-05T16:36:46.031193Z"
      }
    ]
  },
  {
    "title": "업로드 테스트****",
    "author": 2,
    "content": "업로드 테스트****",
    "modified_date": "2016-12-05T16:36:54.173100Z",
    "created_date": "2016-12-05T16:36:54.173136Z",
    "photos": [
      {
        "image": "https://team1-photodiary.s3.amazonaws.com/media/photo/photo/7.jpg",
        "modified_date": "2016-12-05T16:36:54.177514Z",
        "created_date": "2016-12-05T16:36:54.177540Z"
      },
      {
        "image": "https://team1-photodiary.s3.amazonaws.com/media/photo/photo/2.jpg",
        "modified_date": "2016-12-05T16:36:55.800728Z",
        "created_date": "2016-12-05T16:36:55.800767Z"
      }
    ]
  }
]
~~~

author에는 해당 유저의 pk값이 들어가는데 추후 조금 더 직관적으로 나오도록 바꾸겠습니다.


- POST 요청시 올린 글과 그 글의 사진들의 URL를 반환합니다.

입력해야하는 필드 키 이름
>title

>content

>image

>image

>...

이미지 필드에는 실제 사진 파일이 들어갑니다.
이미지 필드 키값은 여러개가 들어가도 되며 안 들어가도 됩니다.



결과값 예시.

~~~
{
  "title": "업로드 테스트****",
  "author": 2,
  "content": "업로드 테스트****",
  "modified_date": "2016-12-05T16:54:13.123386Z",
  "created_date": "2016-12-05T16:54:13.123422Z",
  "photos": [
    {
      "image": "https://team1-photodiary.s3.amazonaws.com/media/photo/photo/7.jpg",
      "modified_date": "2016-12-05T16:54:13.131410Z",
      "created_date": "2016-12-05T16:54:13.131436Z"
    },
    {
      "image": "https://team1-photodiary.s3.amazonaws.com/media/photo/photo/2.jpg",
      "modified_date": "2016-12-05T16:54:15.022858Z",
      "created_date": "2016-12-05T16:54:15.022894Z"
    },
    {
      "image": "https://team1-photodiary.s3.amazonaws.com/media/photo/photo/1.jpg",
      "modified_date": "2016-12-05T16:54:16.842548Z",
      "created_date": "2016-12-05T16:54:16.842583Z"
    }
  ]
}
~~~
- 썸네일 관련
이미지 업로드시 해당 원본이미지와 썸네일 변환 작업이 같이 진행되어 이미지 url이 2가지로 보여지게됩니다. 아직은 썸네일사진 크기 관련해서는 api딴에서는 조정할 수 없습니다.


- GET 요청시 해당 pk값의 글과 사진데이터를 가져옴.

<http://photodiary-dev.ap-northeast-2.elasticbeanstalk.com/post/post-pk>
(post-pk 값에 가져올 글의 pk값을 입력)

~~~
{
  "id": 12,
  "photos": [],
  "title": "12번째제목",
  "content": "12세번째내용",
  "modified_date": "2016-12-06T18:58:56.189932Z",
  "created_date": "2016-12-06T18:58:56.189972Z",
  "author": 1
}
~~~
위의 결과는 post-pk 값에 12를 입력한 결과

- 위와 같은 URL로 'PUT' 요청시 입력할 key값과 data를 적어 보내면 글 내용을 수정할수 있음

> title 열두번째제목수정

> content 열두번째내용수정

~~~
{
  "id": 12,
  "photos": [],
  "title": "열두번째제목수정",
  "content": "열두번째내용수정",
  "modified_date": "2016-12-08T09:15:43.396939Z",
  "created_date": "2016-12-06T18:58:56.189972Z",
  "author": 1
}
~~~


- 위와 같은 URL로 'DELETE' 요청시 해당 pk값의 글과 사진데이터를 삭제함.


## 사진 관련
: 로그인한 해당 유저의 사진들을 볼 수 있습니다.

- GET 요청시 해당 post-pk값의 글의 사진들을 볼수 있다.

<http://photodiary-dev.ap-northeast-2.elasticbeanstalk.com/post/post-pk/photo>

~~~
[
  {
    "image": {
      "full_size": "/media/photo/images-5_tqRWwMK.jpg",
      "medium_square_crop": "/media/__sized__/photo/images-5_tqRWwMK-crop-c0-5__0-5-400x400-70.jpg"
    },
    "post": 6,
    "id": 9
  },
  {
    "image": {
      "full_size": "/media/photo/images_VHkRCJ5.jpg",
      "medium_square_crop": "/media/__sized__/photo/images_VHkRCJ5-crop-c0-5__0-5-400x400-70.jpg"
    },
    "post": 6,
    "id": 10
  }
]
~~~

위의 예시는 post-pk 값에 6 을 대입한 결과

- DELETE 요청시 해당 post-pk값의 글의 사진들을 삭제할수 있다.





=======

## 검색기능
: 해당 url로 get요청을 보내면서 헤더에는 토큰값, 파라미터에는 title(key값), 검색어(value값) 을 집어 넣으면
자신의 글 목록 중 해당 검색어를 포함하는 글 제목인 글들을 반환합니다.

<https://team1-photodiary.s3.amazonaws.com/post/search>


- GET 요청 

입력해야하는 값

키값, 벨류

해더 > Authorization, Token
파라미터 > title, '검색어'


결과값 예시 (검색어 : 짜장면)
~~~
[
  {
    "id": 17,
    "photos": [
      {
        "id": 29,
        "image": {
          "full_size": "https://team1-photodiary.s3.amazonaws.com/media/photo/photo/1.jpg",
          "medium_square_crop": "https://team1-photodiary.s3.amazonaws.com/media/__sized__/photo/photo/1-crop-c0-5__0-5-400x400-70.jpg"
        },
        "modified_date": "2016-12-08T08:51:12.478597Z",
        "created_date": "2016-12-08T08:51:12.478672Z",
        "post": 17
      },
      {
        "id": 30,
        "image": {
          "full_size": "https://team1-photodiary.s3.amazonaws.com/media/photo/photo/9.jpg",
          "medium_square_crop": "https://team1-photodiary.s3.amazonaws.com/media/__sized__/photo/photo/9-crop-c0-5__0-5-400x400-70.jpg"
        },
        "modified_date": "2016-12-08T08:51:14.171946Z",
        "created_date": "2016-12-08T08:51:14.172037Z",
        "post": 17
      }
    ],
    "title": "짜장면 먹고싶다.",
    "content": "오늘날씨좋다",
    "modified_date": "2016-12-08T08:51:12.471421Z",
    "created_date": "2016-12-08T08:51:12.471471Z",
    "author": 2
  },
  {
    "id": 19,
    "photos": [
      {
        "id": 33,
        "image": {
          "full_size": "https://team1-photodiary.s3.amazonaws.com/media/photo/photo/1.jpg",
          "medium_square_crop": "https://team1-photodiary.s3.amazonaws.com/media/__sized__/photo/photo/1-crop-c0-5__0-5-400x400-70.jpg"
        },
        "modified_date": "2016-12-08T08:51:30.979118Z",
        "created_date": "2016-12-08T08:51:30.979181Z",
        "post": 19
      },
      {
        "id": 34,
        "image": {
          "full_size": "https://team1-photodiary.s3.amazonaws.com/media/photo/photo/9.jpg",
          "medium_square_crop": "https://team1-photodiary.s3.amazonaws.com/media/__sized__/photo/photo/9-crop-c0-5__0-5-400x400-70.jpg"
        },
        "modified_date": "2016-12-08T08:51:31.784677Z",
        "created_date": "2016-12-08T08:51:31.784829Z",
        "post": 19
      }
    ],
    "title": "짜장면먹고싶다",
    "content": "오늘날씨좋다",
    "modified_date": "2016-12-08T08:51:30.971914Z",
    "created_date": "2016-12-08T08:51:30.972004Z",
    "author": 2
  }
]
~~~

