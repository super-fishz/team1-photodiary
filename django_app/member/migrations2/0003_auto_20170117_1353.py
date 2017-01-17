# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-17 04:53
from __future__ import unicode_literals

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_myuser_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='profile_img',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='user_profile', verbose_name='profile'),
        ),
    ]
