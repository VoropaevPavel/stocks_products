from rest_framework import serializers
from .models import Product, Stock, StockProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['quantity', 'price', 'product']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']


    def create(self, validated_data):
        positions_data = validated_data.pop('positions')

        stock = super().create(validated_data)
        for position_data in positions_data:
            StockProduct.objects.create(stock=stock, **position_data)
        return stock

    def update(self, instance, validated_data):
        positions_data = validated_data.pop('positions')

        instance = super().update(instance, validated_data)
        instance.stockproduct_set.all().delete()

        for position_data in positions_data:
            StockProduct.objects.create(stock=instance, **position_data)
        return instance