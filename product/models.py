from django.db import models

# Create your models here.
class Product(models.Model):
	age = models.DecimalField(max_digits=5, decimal_places=2)
	name2 = models.CharField(max_length=100)

class User(models.Model):


