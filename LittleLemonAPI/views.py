from rest_framework import generics, status
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated, IsAdminUser, DjangoModelPermissions
from . import models
from . import serializers
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from datetime import date


class CategoriesView(generics.ListCreateAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

class MenuItemsView(generics.ListCreateAPIView):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer
    search_fields = ['title','category']
    ordering_fields = ['price']    
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]



class CartView(generics.ListCreateAPIView):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return models.Cart.objects.all().filter(user = self.request.user)
    
    #TODO add delete function for specific cart menu item beside that one which delete all the items in the cart
    #TODO maybe a patch one to adjust the quantity
    def delete(self,request):
        models.Cart.objects.all().filter(user=self.request.user).delete()
        return Response('ok')

class OrdersView(generics.ListCreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return models.Order.objects.all()
        elif self.request.user.groups.count()==0:
            return models.Order.objects.all().filter(user=self.request.user)
        elif self.request.user.groups.filter(name = 'Delivery Crew').exists():
            return models.Order.objects.all().filter(delivery_crew=self.request.user)
        elif self.request.user.groups.filter(name = 'Manager').exists():
            return models.Order.objects.all()
        
    def create(self, request, *args, **kwargs):
        menuitem_count = models.Cart.objects.all().filter(user=self.request.user).count()
        if menuitem_count == 0:
            return Response({'message':'no items in cart'})
        
        data = request.data.copy()
        total = self.get_total_price(self.request.user)
        data['total']=total
        data['user']=self.request.user.id
        data['date']=date.today()
        order_serilaizer = serializers.OrderSerializer(data=data)
        if order_serilaizer.is_valid(raise_exception=True):
            order = order_serilaizer.save()
            
            items = models.Cart.objects.all().filter(user=self.request.user).all()
            for item in items.values():
                orderitem = models.OrderItem(
                    order=order,
                    menuitem_id=item['menuitem_id'],
                    price = item['price'],
                    quantity = item['quantity']
                )
                orderitem.save()
            
            models.Cart.objects.all().filter(user=self.request.user).delete()
            result = order_serilaizer.data.copy()
            result['total'] = total
            return Response(result)
    
    def get_total_price(self,user):
        total = 0
        items = models.Cart.objects.all().filter(user=user).all()
        for item in items.values():
            total+=item['price']
        return total
            
class SingleOrderView(generics.RetrieveUpdateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes=[IsAuthenticated]
    
    #TODO edit the function so delivery crew can just update the status
    def update(self, request, *args, **kwargs):
        if self.request.user.groups.count()==0:
            return Response('unauthorized',status.HTTP_401_UNAUTHORIZED)
        else:
            return super().update(request, *args, **kwargs)

class GroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]
    def list(self, request):
        users = User.objects.all().filter(groups__name='Manager')
        items = serializers.UserSerializer(users, many=True)
        return Response(items.data)

    def create(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        managers = Group.objects.get(name="Manager")
        managers.user_set.add(user)
        return Response({"message": "user added to the manager group"}, 200)

    def destroy(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        managers = Group.objects.get(name="Manager")
        managers.user_set.remove(user)
        return Response({"message": "user removed from the manager group"}, 200)

class DeliveryCrewViewSet(viewsets.ViewSet):
    permission_classes = [DjangoModelPermissions]
    def list(self, request):
        users = User.objects.all().filter(groups__name='Delivery Crew')
        items = serializers.UserSerializer(users, many=True)
        return Response(items.data)

    def create(self, request):
        #only for super admin and managers
        if self.request.user.is_superuser == False:
            if self.request.user.groups.filter(name='Manager').exists() == False:
                return Response({"message":"forbidden"}, status.HTTP_403_FORBIDDEN)
        
        user = get_object_or_404(User, username=request.data['username'])
        dc = Group.objects.get(name="Delivery Crew")
        dc.user_set.add(user)
        return Response({"message": "user added to the delivery crew group"}, 200)

    def destroy(self, request):
        #only for super admin and managers
        if self.request.user.is_superuser == False:
            if self.request.user.groups.filter(name='Manager').exists() == False:
                return Response({"message":"forbidden"}, status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, username=request.data['username'])
        dc = Group.objects.get(name="Delivery Crew")
        dc.user_set.remove(user)
        return Response({"message": "user removed from the delivery crew group"}, 200)
    

class BookingsView(generics.ListCreateAPIView):
    queryset = models.Booking.objects.all()
    serializer_class = serializers.BookingSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['date']
    
    #TODO add a view to return available slot to book using date send slots for every tabel
    #TODO add a cancel feature for the booking
    #TODO add feature to confirm the booking through email
    def get_queryset(self):
        if self.request.user.groups.count()==0:
            return models.Booking.objects.all().filter(user = self.request.user)
        else :
            return models.Booking.objects.all()