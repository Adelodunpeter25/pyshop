from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=400)
    stock = models.IntegerField(default=0)
    image_url = models.CharField(max_length=24000)
    category = models.CharField(max_length=100, default='General')
    description = models.TextField(blank=True, null=True) 
    subcategory = models.CharField(max_length=100, blank=True, null=True)  

class Offer(models.Model):
    code = models.CharField(max_length=50,)
    description = models.CharField(max_length=255)
    discount = models.FloatField()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add extra fields as needed, e.g.:
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username