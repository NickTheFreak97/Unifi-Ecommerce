from django.db import models
from .category import Category

class Product(models.Model):
    barcode = models.CharField(max_length=127, unique=True, primary_key=True)
    name = models.CharField(max_length=127)
    description = models.TextField()
    datasheet = models.JSONField()
    timeOfCreation = models.DateTimeField()
    timeOfDeletion = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)