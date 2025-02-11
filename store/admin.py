from django.contrib import admin, messages
from django.db.models import Count, QuerySet
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]
    
    def queryset(self, request, queryset : QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

# Register your models here.
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'products_count')
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist') 
            + '?' 
            + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href = "{}">{}</a>', url, collection.products_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )
    
@admin.register(models.Promotion)   
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('description', 'discount_products_link')
    search_fields = ['discount']

    @admin.display(description="Discounted Products")
    def discount_products_link(self, promotion):
        url = (
            reverse('admin:store_product_changelist') 
            + '?' 
            + urlencode({
                'promotion__discount': str(promotion.discount)
            }))
        return format_html('<a href="{}">{}</a>', url, f"{promotion.discount}%")

    def get_queryset(self, request):
        return super().get_queryset(request)

    @admin.display(description="Discount (%)")
    def discount_percentage(self, obj):
        return f"{obj.discount}%"
    

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title']
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    list_display = ['id', 'image', 'title', 'unit_price', 'rating', 'inventory_status', 'collection_title', 'product_discount', 'unit_price_after_discount']  
    list_editable = ['unit_price']
    list_filter = ['collection', 'promotion__discount', 'last_update', InventoryFilter]
    list_select_related = ['collection', 'promotion']
    list_per_page = 10

    def collection_title(self, product):
        return product.collection.title
    
    def product_discount(self, product):
        return f"{product.promotion.discount}%" if product.promotion else "No Discount"
    
    @admin.display(description="Price After Discount")
    def unit_price_after_discount(self, product):
        return f"${product.unit_price_after_discount}"

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory = 0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated. ',
            messages.SUCCESS
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'customer_orders']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    def customer_orders(self, customer):
        url = (reverse('admin:store_order_changelist')
               + '?'
               + urlencode({
                   'customer__id': str(customer.id)
               })
               )
        return format_html('<a href = "{}">{}</a>', url, customer.order_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            order_count = Count('order')
        )


class OrderItemInline(admin.StackedInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    extra = 0
    min_num = 1
    max_num = 10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer_name']
    autocomplete_fields = ['customer']
    ordering = ['placed_at']
    list_select_related = ['customer']
    inlines = [OrderItemInline]
    list_per_page = 10

    def customer_name(self, order):
        return order.customer.first_name + ' ' + order.customer.last_name
    

    