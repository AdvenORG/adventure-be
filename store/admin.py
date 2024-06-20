from typing import Any
from urllib.parse import urlencode

from django.contrib import admin, messages
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html

from . import models

# Register your models here.


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "phone_number", "orders_count"]
    list_editable = ["phone_number"]
    list_per_page = 10
    # ordering = ["first_name", "last_name", "email"]
    search_fields = ["first_name__istartswith", "last_name__istartswith"]

    @admin.display(ordering="orders_count")
    def orders_count(self, customer: models.Customer):
        return customer.orders_count

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(orders_count=Count("order"))


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "products_count"]

    @admin.display(ordering="products_count")
    def products_count(self, category):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"category_id": str(category.category_id)})
        )
        return format_html('<a href="{}">{}</a>', url, category.products_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(products_count=Count("product"))


class StockFilter(admin.SimpleListFilter):
    title = "stock"
    parameter_name = "stock"

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [("<5", "Low"), (">=5", "High")]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == "<5":
            return queryset.filter(stock__lt=5)
        if self.value() == ">=5":
            return queryset.filter(stock__gte=5)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "product_id",
        "SKU",
        "slug",
        "description",
        "price",
        "stock",
        "inventory_status",
        "category_name",
    ]
    list_editable = ["price"]
    list_per_page = 10
    list_select_related = ["category"]
    list_filter = ["category", StockFilter]
    actions = ["clear_stock"]

    def category_name(self, product: models.Product):
        return product.category.name

    @admin.display(ordering="stock")
    def inventory_status(self, product: models.Product):
        if product.stock < 5:
            return "Low"
        return "OK"

    @admin.action(description="Clear stock")
    def clear_stock(self, request, queryset: QuerySet[Any]):
        update_count = queryset.update(stock=0)
        self.message_user(
            request,
            f"{update_count} products were successfully updated.",
            messages.ERROR,
        )


@admin.register(models.Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = [
        "wishlist_id",
        "customer",
        "product",
    ]


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [
        "card_id",
        "quality",
        "customer",
        "product",
    ]


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "payment_id",
        "payment_date",
        "payment_method",
        "amount",
        "customer",
    ]


@admin.register(models.Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = [
        "shipment_id",
        "shipment_date",
        "address",
        "city",
        "state",
        "country",
        "zip_code",
        "customer",
    ]


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_id",
        "order_date",
        "total_price",
        "customer",
        "shipment",
        "payment",
    ]
    ordering = ["customer", "order_date", "total_price"]
    list_per_page = 10


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "order_item_id",
        "quantity",
        "price",
        "order_date",
        "product",
        "customer",
    ]
    list_per_page = 10
    list_select_related = ["order", "product"]

    def order_date(self, order_item: models.OrderItem):
        return str(order_item.order.order_date)

    def customer(self, order_item: models.OrderItem):
        return order_item.order.customer
