import os

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import default_storage
from django.db import models

from app.ftp_utils import upload_file


class ImageManager(models.Manager):
    def for_model(self, model_instance):
        content_type = ContentType.objects.get_for_model(model_instance)
        return self.filter(content_type=content_type, object_id=model_instance.pk)

    def for_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return self.filter(content_type=content_type, object_id=instance.pk)

    def add_image(self, model_instance, image, description=""):
        content_type = ContentType.objects.get_for_model(model_instance)
        return self.create(
            content_type=content_type,
            object_id=model_instance.id,
            image=image,
            description=description,
        )


class Image(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    image = models.ImageField(upload_to="images/")
    description = models.CharField(max_length=255, blank=True, null=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    objects = ImageManager()

    def __str__(self):
        return f'{self.content_object} - {self.description or "Image"}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        local_file_path = self.image.path
        base_name = os.path.basename(local_file_path)
        content_type_folder = self.content_type.model
        remote_file_path = f"images/{content_type_folder}/{base_name}"
        upload_file(local_file_path, remote_file_path)
        if default_storage.exists(local_file_path):
            default_storage.delete(local_file_path)
        self.image.name = remote_file_path
        super().save(update_fields=["image"])

    @property
    def image_url(self):
        return default_storage.url(self.image.name)
