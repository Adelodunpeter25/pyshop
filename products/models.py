from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image_url = models.URLField(max_length=2000)
    category = models.CharField(max_length=100, default='General', db_index=True)
    description = models.TextField(blank=True, null=True) 
    subcategory = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['category', 'subcategory']),
            models.Index(fields=['price']),
        ]
    
    def __str__(self):
        return self.name  

class Offer(models.Model):
    code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} - {self.discount}%"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add extra fields as needed, e.g.:
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username