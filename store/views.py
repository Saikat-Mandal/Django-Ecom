from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import ProductSerializer,CollectionSerializer
from .models import Product , Collection

        
class ProductList   (APIView):

    def get(self,request):
        q = Product.objects.select_related('collection').all() #serialize
        serializer = ProductSerializer(q , many=True , context={'request': request})
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ProductSerializer(data = request.data) #deseralize
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)           


class ProductDetail(APIView):

    def get(self , id):
        product = get_object_or_404(Product ,pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data , status=status.HTTP_200_OK)

    def put(self , request , id):
        product = get_object_or_404(Product ,pk=id)
        serializer = ProductSerializer( product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)        
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)     

    def delete(self, id):
        product = get_object_or_404(Product ,pk=id)
        if product.orderitems.count() > 0: # type: ignore
                 return Response('Please remove the necessary order item' , status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response("deleted succesfully" ,status=status.HTTP_204_NO_CONTENT)        
            


@api_view(['GET' , 'POST'])
def collection_list(request):
    
    if request.method == 'GET':
        q = Collection.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionSerializer(q , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)  
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET' , 'PUT' , 'DELETE'])
def collection_detail(request , pk):
    c = get_object_or_404(Collection.objects.annotate(products_count=Count('products')) , pk=pk)

    if request.method == 'GET':
        serializer = CollectionSerializer(c)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = CollectionSerializer(c , data=request.data)
        if serializer.is_valid():
             serializer.save()
             return Response(serializer.data , status=status.HTTP_200_OK) 

    elif request.method == 'DELETE':
        if c.products.count() > 0: # type: ignore
            return Response({'error' : 'cannot delete'})
        c.delete()
        return Response("deleted succesfully" ,status=status.HTTP_204_NO_CONTENT)  
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
