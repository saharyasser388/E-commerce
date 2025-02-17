from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']
    

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.IntegerField()

    def __str__(self) -> str:
        return (str(self.discount)+'%')
    

class Product(models.Model):
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, null=True, blank=True)
    model = models.CharField(max_length=255, null=True, blank=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField()
    popular = models.BooleanField(null=True, blank=True)
    rating = models.FloatField(null = True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField (
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)]
        )
    inventory = models.IntegerField(validators=[MinValueValidator(1)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotion = models.ForeignKey(Promotion,  on_delete=models.PROTECT, null=True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']

    @property
    def price_after_discount(self):
        if self.promotion:
            discount_amount = (self.price * self.promotion.discount) / 100
            return round(self.price - discount_amount, 2)  # Rounded to 2 decimal places
        return self.price  # No discount applied
    
    @property
    def on_sale(self):
        return (self.promotion and self.promotion.discount > 0 )

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    

class Address(models.Model):
    street = models.CharField(max_length=255)
    city  = models.CharField(max_length=255)
    zip = models.CharField(max_length=255, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Order(models.Model):
    PENDIND_STATE = 'P'
    COMPLETE_STATE = 'C'
    FAILD_STATE = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PENDIND_STATE, 'Pending'),
        (COMPLETE_STATE, 'Complete'),
        (FAILD_STATE, 'Failed')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,  choices=PAYMENT_STATUS_CHOICES, default=PENDIND_STATE)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"
    
    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        unique_together = [['cart', 'product']]








