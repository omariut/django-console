from rest_framework import serializers  
from product import models as product_models 

 
class ProductSerializer(serializers.ModelSerializer):

	class Meta:
		model = product_models.Product
		fields = '__all__'


