from django.urls import path
from product import views
 
urlpatterns = [
    path('product/list/', views.ProductListView.as_view(), name='product_list'),
    path('product/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
]


urlpatterns = [
    path('products/', views.ProductListCreateAPIView.as_view(), name='product_list_create'),
    path('products/<int:pk>', views.ProductRetrieveUpdateDestroyAPIView.as_view(), name='product_retrieve_update_destroy'),
]


