from rest_framework import serializers 
 
class ProductSerializer(serializers.ModelSerializer):
	model = Product
	fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
	model = User
	fields = '__all__'
