from django.urls import path
from product import views
 
urlpatterns = [
    path('products/', views.ProductListCreateAPIView.as_view(), name='product_list_create'),
    path('products/<int:pk>', views.ProductRetrieveUpdateDestroyAPIView.as_view(), name='product_retrieve_update_destroy'),
]


