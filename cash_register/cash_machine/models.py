from django.db import models
from django.utils import timezone

class Item(models.Model):
    title = models.CharField(max_length=255, blank=True)
    price = models.FloatField(blank=True)

class Receipt(models.Model):
    datetime = models.DateTimeField()
    data = models.JSONField(default=dict, blank=True)