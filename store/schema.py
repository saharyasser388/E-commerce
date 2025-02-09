import strawberry
from typing import List, Optional
from .models import Product, Collection, Promotion
from .types import ProductType
from .scalars import Upload
from django.core.exceptions import ObjectDoesNotExist


#Query[Get - Read]
@strawberry.type
class Query:
    @strawberry.field
    def get_products(self) -> List[ProductType]:
        return Product.objects.all()
    
    @strawberry.field
    def get_product(self, id: int) -> Optional[ProductType]:
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None


#Mutation[Create - Update - Delete]
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_product(
        self, 
        image: Upload, 
        title: str, 
        slug: str, 
        rating: float, 
        description: str, 
        unit_price: float, 
        inventory: int, 
        collection_title: str, 
        promotion_discount: Optional[int] = None) -> ProductType:
        try:
            collection = Collection.objects.get(title=collection_title)
        except ObjectDoesNotExist:
            collection = Collection.objects.create(title=collection_title)

        promotion = None
        if promotion_discount is not None:  # Only fetch if a discount is provided
            try:
                promotion = Promotion.objects.get(discount=promotion_discount)
            except ObjectDoesNotExist:
                promotion = Promotion.objects.create(discount=promotion_discount)
        
        product = Product.objects.create(
            image=image,
            title=title,
            slug=slug,
            rating=rating,
            description=description,
            unit_price=unit_price,
            inventory=inventory,
            collection=collection,
            promotion=promotion
        )
        return product

    @strawberry.mutation
    def update_product(
        self,
        id: int,
        image: Upload,
        title: Optional[str] = None,
        slug: Optional[str] = None,
        rating: Optional[float] = None,
        description: Optional[str] = None,
        unit_price: Optional[float] = None,
        inventory: Optional[int] = None
    ) -> ProductType:
        product = Product.objects.get(id=id)
        
        if image is not None:
            product.image = image
        if title is not None:
            product.title = title
        if slug is not None:
            product.slug = slug
        if rating is not None:
            product.rating = rating
        if description is not None:
            product.description = description
        if unit_price is not None:
            product.unit_price = unit_price
        if inventory is not None:
            product.inventory = inventory
        
        product.save()
        return product
    
    @strawberry.mutation
    def delete_product(self, id: int) -> Optional[ProductType]:
        try:
            product = Product.objects.get(id=id)

            deleted_product = ProductType(
                id=product.id,
                title=product.title,
                slug=product.slug,
                rating=product.rating,
                description=product.description,
                unit_price=product.unit_price,
                inventory=product.inventory,
                collection=product.collection.title if product.collection else None,  
                promotion=product.promotion.discount if product.promotion else None  
            )

            product.delete()
            return deleted_product  

        except ObjectDoesNotExist:
            return None  


schema = strawberry.Schema(query=Query, mutation=Mutation)