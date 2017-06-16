from __future__ import unicode_literals

from django.db import models

from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes.fields import GenericRelation

from hitcount.models import HitCount, HitCountMixin

# Create your models here.

from django.db import models
from django.utils import timezone

@python_2_unicode_compatible
class Post(models.Model, HitCountMixin):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
