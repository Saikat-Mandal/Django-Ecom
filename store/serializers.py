from rest_framework import serializers
from .models import Product ,Collection


# Collection serializer 
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model =Collection
        fields= ['id' , 'title']


# product serializer 
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id' , 'title' , 'unit_price' , 'price_with_tax' , 'collection']

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    def calculate_tax(self , product):
        return product.unit_price +200
