from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^member/', include('member.urls', namespace='member')),
    url(r'^post/', include('post.urls', namespace='post')),

]
