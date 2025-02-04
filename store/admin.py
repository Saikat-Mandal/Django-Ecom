from typing import Any
from django.contrib import admin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.html import format_html 
from urllib.parse import urlencode
from . import models


# FILTERS 
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10' , 'Low')
        ]
    
    def queryset(self, request, queryset):
        if self.value == '<10':
            return queryset.filter(inventory__lt=10)



# collection 
@admin.register(models.Collection)
class Collection(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self,collection):
        url = (reverse('admin:store_product_changelist') 
               + '?'
               + urlencode({
                   'collection__id' : str(collection.id)
               }))
        return format_html('<a href="{}">{}</a>' , url,collection.products_count)
        
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )
        


# customer 
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name' , 'last_name', 'membership' , 'orders_count']  
    list_editable = ['membership']
    list_per_page = 10

    def orders_count(self,customer):
        return customer.orders_count
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        ) 
    

# inline order item class 
class OrderItemInline(admin.StackedInline):
    model = models.OrderItem
    extra = 0


# order 
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id' , 'placed_at' , 'customer']
    inlines = [OrderItemInline]

    
# product 
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions =['clear_inventory']
    list_display = ['title' , 'unit_price' , 'inventory_status' , 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_filter = ['collection' , 'last_update' , InventoryFilter] #filter
    list_select_related = ['collection']

    def collection_title(self , product ): #a new field
        return product.collection.title

    @admin.display(ordering='inventory') #ordering 
    def inventory_status(self,product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    
    @admin.action(description='Clear inventory')
    def clear_inventory(self , request , queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were succesfully updated'
        )