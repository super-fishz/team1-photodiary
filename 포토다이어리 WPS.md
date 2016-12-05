

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
email
password

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


## 사진 관련