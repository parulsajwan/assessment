# models.py
from django.db import models


class Product(models.Model):
    product_id = models.CharField(max_length=50, unique=True)
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.FloatField()
    quantity_sold = models.IntegerField()
    rating = models.FloatField()
    review_count = models.IntegerField()

    def __str__(self):
        return f"{self.product_id} | {self.product_name}"
