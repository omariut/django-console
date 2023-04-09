from django.db import models

# Create your models here.
class Product(models.Model):

	price = models.IntegerField()
	age = models.IntegerField()



