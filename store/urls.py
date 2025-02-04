from django.urls import path , include
from . import views
urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<int:id>/', views.ProductDetail.as_view() ),
    path('collections/<int:pk>/', views.collection_detail  , name='collection-detail'),
    path('collections/',views.collection_list )
]
