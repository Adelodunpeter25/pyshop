from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=400)
    stock = models.IntegerField()
    image_url = models.CharField(max_length=24000)
    category = models.CharField(max_length=100, default='General')
    description = models.TextField(blank=True, null=True) 
    subcategory = models.CharField(max_length=100, blank=True, null=True)  

class Offer(models.Model):
    code = models.CharField(max_length=50,)
    description = models.CharField(max_length=255)
    discount = models.FloatField()