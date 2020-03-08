# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-07-17 23:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmark', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='tags',
            field=models.ManyToManyField(through='bookmark.BookmarkTag',
                                         to='bookmark.Tag'),
        ),
    ]
