from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    price = serializers.FloatField()

    def create(self, validated_data):
        return Item.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.price = validated_data.get('price', instance.price)

        instance.save()
        return instance

