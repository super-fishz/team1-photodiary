from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^user/', UserList.as_view()),
    url(r'^user_detail/$', CurrentUserDetail.as_view()),
    url(r'^auth/', include('rest_auth.urls'))
]
