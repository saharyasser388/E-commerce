import strawberry
from typing import List, Optional

import strawberry.django
from . import models

@strawberry.django.type(models.Collection)
class Collection:
    title: str

@strawberry.django.type(models.Promotion)
class Promotion:
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
    collection: Optional[Collection]
    promotion: Optional[Promotion]

    @strawberry.field
    def image(self) -> Optional[str]:
        return self.image.url if self.image else None
    
    @strawberry.field
    def unit_price_after_discount(self) -> float:
        """Compute the price after applying the discount."""
        if self.promotion:
            discount_amount = (self.unit_price * self.promotion.discount) / 100
            return round(self.unit_price - discount_amount, 2)
        return self.unit_price  # No discount applied

