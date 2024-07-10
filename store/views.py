from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProductSerializer
from .models import Product
# Create your views here.

@api_view(['GET' , 'POST'])
def product_list(request):
    if request.method == 'GET':
        q = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(q , many=True , context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.validated_data
            return Response('ok')
    return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)            
        

@api_view(['GET'])
def product_detail(request , id):
        product = get_object_or_404(Product ,pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)  

@api_view(['GET'])
def collection_detail(request , pk):
      return Response('ok')
      
