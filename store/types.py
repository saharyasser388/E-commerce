import strawberry
from typing import List, Optional
import strawberry.django
from . import models
from datetime import datetime
from django.contrib.auth.models import User

@strawberry.django.type(User)
class UserType:
    id: strawberry.ID
    first_name: str
    last_name: str
    email: str

@strawberry.django.type(models.Collection)
class CollectionType:
    title: str

@strawberry.django.type(models.Promotion)
class PromotionType:
    discount: Optional[int]

@strawberry.django.type(models.Product)
class ProductType:
    id: int
    title: str
    slug: str
    rating: Optional[float]
    description: str
    unit_price: float
    inventory: int
    collection: Optional[CollectionType]
    promotion: Optional[PromotionType]

    @strawberry.field
    def image(self) -> Optional[str]:
        return self.image.url if self.image else None
    
    @strawberry.field
    def unit_price_after_discount(self) -> float:
        if self.promotion:
            discount_amount = (self.unit_price * self.promotion.discount) / 100
            return round(self.unit_price - discount_amount, 2)
        return self.unit_price 

@strawberry.django.type(models.CartItem)
class CartItemType:
    product: ProductType
    product_id: int
    quantity: int

    @strawberry.field
    def product_name(self) -> str:
        return self.product.title
    
    @strawberry.field
    def product_price(self) -> float:
        if self.product.promotion:
            discount_amount = (self.product.unit_price * self.product.promotion.discount) / 100
            return round(self.product.unit_price - discount_amount, 2)
        else:
            return self.product.unit_price
    
    @strawberry.field
    def discount(self) -> float:
        return self.product.promotion.discount if self.product.promotion else 0

@strawberry.django.type(models.Cart)
class CartType:
    id: int
    items: List[CartItemType]

    @strawberry.field
    def total_price(self) -> float:
        total = 0
        for item in self.items.all():
            if item.product.promotion:
                discount_amount = (item.product.unit_price * item.product.promotion.discount) / 100
                total +=  (round(item.product.unit_price - discount_amount, 2) * item.quantity)
            else:
                total += (item.product.unit_price * item.quantity)
        return total


@strawberry.django.input(models.CartItem)
class CartItemInput:
    product_id: int
    quantity: int


