from versatileimagefield.fields import VersatileImageField
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=200, blank=True)
    author = models.ForeignKey('member.MyUser', null=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Photo(models.Model):
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    image = VersatileImageField('image', upload_to='photo', blank=False)
    post = models.ForeignKey(Post, null=True)

    def __str__(self):
        return 'POST(%s) - PHOTO(%s)' % (self.post.pk, self.pk)


class TodayPhoto(models.Model):
    image = VersatileImageField('image', upload_to='today', blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    author = models.ForeignKey('member.MyUser', related_name='photo_set_author', null=True, blank=True)
    used_date = models.DateTimeField(blank=True, null=True)
    is_good = models.BooleanField(default=False)
    is_bad = models.BooleanField(default=False)
    is_not_know = models.BooleanField(default=False)
    select_users = models.ManyToManyField('member.MyUser',
                                          through='SelectTodayPhoto',
                                          related_name='photo_set_select_users')
    select_count = models.SmallIntegerField(default=0)


class SelectTodayPhoto(models.Model):
    user = models.ForeignKey('member.MyUser')
    photo = models.ForeignKey(TodayPhoto)
    created_date = models.DateTimeField(auto_now_add=True)
