from django.contrib import admin

from .models import LikeItem

# Register your models here.


@admin.register(LikeItem)
class LikeItemAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "user",
        "content_type",
        "object_id",
        "content_object",
        "comment",
    ]
