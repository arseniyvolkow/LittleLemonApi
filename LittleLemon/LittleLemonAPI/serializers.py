from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.shortcuts import get_object_or_404
from datetime import datetime


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['slug', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='title', queryset=Category.objects.all())

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['menuitem', 'quantity', 'price']


class CartAddItemsSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = Cart
        fields = ['menuitem', 'quantity']


class OrderItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='menuitem.title', read_only=True)
    unit_price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='menuitem.price', read_only=True)
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['name', 'quantity', 'unit_price', 'price']
        extra_kwargs = {
            'menuitem': {'read_only': True}
        }


class OrdersSerializer(serializers.ModelSerializer):
    Date = serializers.SerializerMethodField()
    date = serializers.DateTimeField(write_only=True, default=datetime.now)
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status',
                  'total', 'Date', 'date', 'order_items']
        extra_kwargs = {
            'total': {'read_only': True}
        }

    def get_Date(self, obj):
        return obj.date.strftime('%Y-%m-%d')

    def get_order_items(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        serializer = OrderItemSerializer(order_items, many=True, context={
                                         'request': self.context['request']})
        return serializer.data


class OrdersPutSerializer(serializers.ModelSerializer):
    class Meta():
        model = Order
        fields = ['delivery_crew']
