from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey



class Tag(models.Model):
    label = models.TextField(max_length=255)

class TagItem(models.Model):

    ###
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    ###
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

