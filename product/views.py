class ProductListView(generic.ListView):
	model = Product
	paginate_by = 10
class ProductCreateView(generic.CreateView):
	model = Product
	fields = '__all__'
	success_url= ' \ ' 
class ProductDetailView(generic.DetailView):
	model = Product
