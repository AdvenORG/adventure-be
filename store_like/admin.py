from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html

from images.models import Image
from like.models import LikeItem
from store.admin import ProductAdmin
from store.models import Product

# Register your models here.


class LikeItemInLine(GenericTabularInline):
    model = LikeItem
    autocomplete_fields = ["user"]


class ImageInLine(GenericTabularInline):
    model = Image

    fields = ["image", "image_tag", "description"]
    readonly_fields = ["image_tag", "uploaded_at"]

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<div class="field-image"><img src="{}" width="100" height="100" /></div>',
                obj.image_url,
            )
        return ""

    image_tag.short_description = "Image"


class CustomProductAdmin(ProductAdmin):
    inlines = [LikeItemInLine, ImageInLine]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
