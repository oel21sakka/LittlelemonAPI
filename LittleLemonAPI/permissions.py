from rest_framework import permissions
from rest_framework.authtoken.models import Token

class ManagerPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        token = request.META.get('HTTP_AUTHORIZATION')[6:]
        user = Token.objects.get(key = token).user
        return user.groups.filter(name = 'Manager').exists()
    
    
class CustomerPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        token = request.META.get('HTTP_AUTHORIZATION')[6:]
        user = Token.objects.get(key = token).user
        return user.groups.filter(name = 'Customer').exists()