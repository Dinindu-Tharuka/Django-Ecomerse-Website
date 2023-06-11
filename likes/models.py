from django.db import models
from django.conf import settings
from store_custom.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class LikedItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, models.CASCADE)
    object_id = models.PositiveIntegerField()
    object_type = GenericForeignKey()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      