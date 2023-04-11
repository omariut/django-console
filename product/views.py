from django.views import generic 
from product import models as product_models 
from rest_framework import generics 
from product import serializers

 
class ProductListView(generic.ListView):
	model =  product_models.Product
	paginate_by = 10 



class ProductCreateView(generic.CreateView):
	model = product_models.Product
	fields = '__all__'
	success_url= ' \ ' 


class ProductDetailView(generic.DetailView):
	model =  product_models.Product 



class ProductListCreateAPIView(generics.ListCreateAPIView):
	serializer_class = serializers.ProductSerializer
	queryset = product_models.Product.objects.filter().select_related().prefetch_related()
	#authentication_classes=()


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = serializers.ProductSerializer
	queryset = product_models.Product.objects.filter().select_related().prefetch_related()
	#authentication_classes=()


