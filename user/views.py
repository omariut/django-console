from django.views import generic 
from user import models as user_models 
from rest_framework import generics 
from user import serializers

 
class UserListView(generic.ListView):
	model =  user_models.User
	paginate_by = 10 



class UserCreateView(generic.CreateView):
	model = user_models.User
	fields = '__all__'
	success_url= ' \ ' 


class UserDetailView(generic.DetailView):
	model =  user_models.User 



class UserListCreateAPIView(generics.ListCreateAPIView):
	serializer_class = serializers.UserSerializer
	queryset = user_models.User.objects.filter().select_related().prefetch_related()
	#authentication_classes=()


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = serializers.UserSerializer
	queryset = user_models.User.objects.filter().select_related().prefetch_related()
	#authentication_classes=()


