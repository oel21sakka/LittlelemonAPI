from rest_framework import serializers
from . import models
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['id','username','email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta():
        model = models.Category
        fields = ['id','title','slug']


class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset = models.Category.objects.all())
    class Meta():
        model = models.MenuItem
        fields = ['id', 'title', 'price', 'category', 'featured']
        
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.OrderItem
        fields = ['order','menuitem','quantity','price']
        
class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many = True, read_only = True, source = 'order')

    class Meta():
        model = models.Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'date', 'total', 'order_items']        
    
class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(),default = serializers.CurrentUserDefault())
    
    def validate(self,attrs):
        attrs['unit_price'] = attrs['menuitem'].price
        attrs['price'] = attrs['quantity'] * attrs['unit_price']
        return attrs
    
    class Meta():
        model = models.Cart
        fields = ['user', 'menuitem', 'unit_price', 'quantity', 'price']
        extra_kwargs = {
            'price': {'read_only': True},
            'unit_price': {'read_only': True}            
        }    
    
    
class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(),default = serializers.CurrentUserDefault())
    
    class Meta():
        model = models.Booking
        fields = ['user','date','slot','tabel','num_of_guests']