from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.


class LikeItemManager(models.Manager):
    
    
    def get_likes_for(self, object_type: models.Model, object_id: int):
        content_type = ContentType.objects.get_for_model(object_type)
        return LikeItem.objects.filter(content_type=content_type, object_id=object_id)


class LikeItem(models.Model):
    objects = LikeItemManager()
    comment = models.CharField(max_length=255, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"
