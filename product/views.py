from django.views import generic 
from product import models as product_models 
from rest_framework import generics 
from product import serializers

 
class ProductListCreateAPIView(generics.ListCreateAPIView):
	serializer_class = serializers.ProductSerializer
	queryset = product_models.Product.objects.filter().select_related().prefetch_related()
	#authentication_classes=()


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = serializers.ProductSerializer
	queryset = product_models.Product.objects.filter().select_related().prefetch_related()
	#authentication_classes=()


