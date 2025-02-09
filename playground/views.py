from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from store.models import *
from tags.models import ContentType, Tag, TaggedItem
# Create your views here.
#request -> response
#request handler
#action
# @transaction.atomic
def say_hello(request):
    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order_id = 1
        item.product_id = 1
        item.quantity = 1
        item.unit_price = 10
        item.save()
    
    

    
    return render(request, 'hello.html', {'name' : 'Sahar'}) 