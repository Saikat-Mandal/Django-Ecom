from django.contrib import admin
from store.models import Product
from store.admin import ProductAdmin
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericStackedInline


# generic tag inline class 
class TagInline(GenericStackedInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    extra = 1

class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]

admin.site.unregister(Product)    
admin.site.register(Product , CustomProductAdmin)   