from django.db import models

# Create your models here.
class Product(models.Model):
	name = models.CharField(max_length=100)
	user = models.ForeignKey(to=User, on_delete=models.CASCADE)

