from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class CommentManager(models.Manager):
    def filter_by_instance(self, instance):

        # Gets the type and id from the instance of Article that is needed for the comments
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        comments = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id)
        return comments



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    def __str__(self):
        return str(self.user.username)

