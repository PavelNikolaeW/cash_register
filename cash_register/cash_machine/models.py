from django.db import models

class Item(models.Model):
    title = models.CharField(max_length=255, blank=True)
    price = models.FloatField(blank=True)
