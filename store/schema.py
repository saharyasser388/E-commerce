import strawberry
from strawberry.types import Info
from typing import List, Optional
from .models import Product, Collection, Promotion, Cart, CartItem
from .types import ProductType, CartItemType, CartType, CartItemInput, UserType
from .scalars import Upload
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login



#Query[Get - Read]
@strawberry.type
class Query: 
    @strawberry.field
    def get_user(self, id: strawberry.ID) -> UserType:
        return User.objects.get(id=id)
    
    @strawberry.field
    def get_users(self) -> List[UserType]:
        return User.objects.all()

    @strawberry.field
    def get_products(self) -> List[ProductType]:
        return Product.objects.all()
    
    @strawberry.field
    def get_product(self, id: int) -> Optional[ProductType]:
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None
        
    @strawberry.field
    def get_cart(self, id: int) -> CartType:
        try:
            return Cart.objects.prefetch_related("items").get(id=id)  
        except Cart.DoesNotExist:
            raise Exception("Cart not found")
        
    


#Mutation[Create - Update - Delete]
@strawberry.type
class Mutation:
    @strawberry.mutation
    def register(
        self, 
        first_name: str, 
        last_name: str, 
        email: str, 
        password: str) -> UserType:

        try:
            validate_email(email)  
        except ValidationError:
            raise ValueError("Invalid email format")

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email,  
            password=password
        )

        return UserType(id=user.id, first_name=user.first_name, last_name=user.last_name, email=user.email)

    @strawberry.mutation
    def login(self, email: str, password: str) -> UserType:
        user = authenticate(username=email, password=password)
        
        if not user:
            raise ValueError("Invalid credentials")

        return UserType(id=user.id, first_name=user.first_name, last_name=user.last_name, email=user.email)

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
        
    @strawberry.mutation
    def create_cart(self) -> CartType:
        cart = Cart.objects.create()
        return cart

    @strawberry.django.mutation
    def delete_cart(self, id: int) -> Optional[CartType]:
        try:
            cart = Cart.objects.get(id=id)
            cart.delete()
            return None  # Return None to indicate successful deletion
        except Cart.DoesNotExist:
            raise Exception(f"Cart with id {id} does not exist")
        
    @strawberry.django.mutation
    def add_to_cart(info, cart_id: int, item_data: CartItemInput) -> CartType:
        try:
            cart = Cart.objects.get(pk=cart_id)
        except Cart.DoesNotExist:
            raise ValueError("Cart not found")

        product = Product.objects.get(pk=item_data.product_id)

        existing_item = cart.items.filter(product=product).first()

        if existing_item:
            existing_item.quantity += item_data.quantity
            existing_item.save()
        else:
            cart_item = CartItem(
                cart=cart,
                product=product,
                quantity=item_data.quantity,
            )
            cart_item.save()

        cart.refresh_from_db() 
        return cart
        

    





    

schema = strawberry.Schema(query=Query, mutation=Mutation)