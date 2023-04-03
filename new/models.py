from django.db import models

# Create your models here.
class Product(models.Model):
	price = models.FloatField()
	name = models.CharField(name='max_length', value='100')
	user = models.ForeignKey(name='to', value='Model-Name', name='on_delete', value='models.CASCADE')

