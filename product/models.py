from django.db import models

# Create your models here.
class Product(models.Model):

	price = models.FloatField()

	class Meta: 
		abstract=True
		ordering=['pub']



