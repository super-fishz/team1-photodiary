from versatileimagefield.fields import VersatileImageField
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=200, blank=True)
    author = models.ForeignKey('member.MyUser', null=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Photo(models.Model):
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    image = VersatileImageField('image', upload_to='photo/photo', blank=False)
    post = models.ForeignKey(Post, null=True)

    def __str__(self):
        return 'POST(%s) - PHOTO(%s)' % (self.post.pk, self.pk)
