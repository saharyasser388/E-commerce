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
    image: Optional[str]
    title: str
    brand: Optional[str]
    model: Optional[str]
    color: Optional[str]
    popular: Optional[bool]
    slug: str
    rating: Optional[float]
    description: str
    price: float
    inventory: int
    collection: Optional[CollectionType]
    promotion: Optional[PromotionType]

    
    @strawberry.field
    def price_after_discount(self) -> float:
        if self.promotion:
            discount_amount = (self.price * self.promotion.discount) / 100
            return round(self.price - discount_amount, 2)
        return self.price 
    
    @strawberry.field
    def on_sale(self) -> bool:
        return bool(self.promotion and self.promotion.discount > 0 )
    

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
            discount_amount = (self.product.price * self.product.promotion.discount) / 100
            return round(self.product.price - discount_amount, 2)
        else:
            return self.product.price
    
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
                discount_amount = (item.product.price * item.product.promotion.discount) / 100
                total +=  (round(item.product.price - discount_amount, 2) * item.quantity)
            else:
                total += (item.product.price * item.quantity)
        return total


@strawberry.django.input(models.CartItem)
class CartItemInput:
    product_id: int
    quantity: int


