urlpatterns+= [
    path('products/', ProductListCreateAPIView.as_view(), name='product_list_create'),
    path('products/<int:pk>', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product_retrieve_update_destroy'),
]


urlpatterns+= [
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]


