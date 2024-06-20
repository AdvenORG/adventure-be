from enum import Enum

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = PhoneNumberField()

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name

    class Meta:
        indexes = [models.Index(fields=["last_name", "first_name"])]


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name", "category_id"]


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    SKU = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.description

    class Meta:
        ordering = ["description", "product_id"]


class Wishlist(models.Model):
    wishlist_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Cart(models.Model):
    card_id = models.AutoField(primary_key=True)
    quality = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class PaymentMethod(Enum):
    C = "CASH"
    M = "MOMO"
    V = "VISA"


class Payment(models.Model):
    payment_id = models.IntegerField()
    payment_date = models.DateField(null=False)
    payment_method = models.CharField(
        max_length=4,
        choices=[(choice.value, choice.name) for choice in PaymentMethod],
        default=(PaymentMethod.C.value, PaymentMethod.C.name),
    )
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return str(self.payment_date)


class Shipment(models.Model):
    shipment_id = models.AutoField(primary_key=True)
    shipment_date = models.DateField()
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.city


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_date = models.DateField(null=False, auto_now_add=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    shipment = models.ForeignKey(Shipment, on_delete=models.PROTECT)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return str(self.order_id)


class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.order_item_id)
