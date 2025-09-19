#!/usr/bin/env python3
"""
Performance monitoring script for PyShop
"""
import os
import sys
import django
import time
from django.db import connection

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyshop.settings')
django.setup()

from products.models import Product

def check_database_performance():
    """Check database query performance"""
    print("=== Database Performance Check ===")
    
    # Test basic query
    start_time = time.time()
    count = Product.objects.count()
    query_time = time.time() - start_time
    print(f"Product count: {count} (Query time: {query_time:.4f}s)")
    
    # Test filtered query
    start_time = time.time()
    electronics = Product.objects.filter(category='Electronics').count()
    query_time = time.time() - start_time
    print(f"Electronics count: {electronics} (Query time: {query_time:.4f}s)")
    
    # Test search query
    start_time = time.time()
    search_results = Product.objects.filter(name__icontains='phone').count()
    query_time = time.time() - start_time
    print(f"Phone search results: {search_results} (Query time: {query_time:.4f}s)")
    
    # Show query count
    print(f"Total queries executed: {len(connection.queries)}")

def check_data_integrity():
    """Check data integrity"""
    print("\n=== Data Integrity Check ===")
    
    # Check for products with invalid prices
    invalid_prices = Product.objects.filter(price__lt=0).count()
    print(f"Products with negative prices: {invalid_prices}")
    
    # Check for products without names
    no_name = Product.objects.filter(name__isnull=True).count()
    print(f"Products without names: {no_name}")
    
    # Check categories
    categories = list(set(Product.objects.values_list('category', flat=True)))
    print(f"Categories: {categories}")

if __name__ == "__main__":
    check_database_performance()
    check_data_integrity()
    print("\n=== Performance Check Complete ===")