from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


def upload_location(instance, filename):
    return "%s/%s" % (instance.title, filename)


class BlogItemModel(models.Model):

    class Meta(object):
        verbose_name = u"Blog Article"

    author = models.ForeignKey(
        User,
    )

    title = models.CharField(
        max_length=255,
        blank=False
    )
    title_image = models.ImageField(
        upload_to=upload_location,
        blank=True,
        verbose_name=u"Cover Image"
    )
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.title
