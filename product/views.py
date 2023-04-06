from django.shortcuts import render

# Create your views here.
class ProductListCreateAPIView(generics.ListCreateAPIView):
	serializer_class = serializers.ProductSerializer
	queryset = Product.objects.filter().select_related().prefetch_related()
	#authentication_classes=()


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = serializers.ProductSerializer
	queryset = Product.objects.filter().select_related().prefetch_related()
	#authentication_classes=()


class ProductListView(generic.ListView):
	model = Product
	paginate_by = 10 



class ProductCreateView(generic.CreateView):
	model = Product
	fields = '__all__'
	success_url= ' \ ' 


class ProductDetailView(generic.DetailView):
	model = Product 



