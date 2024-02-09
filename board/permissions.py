from rest_framework.permissions import BasePermission

from board.choices import RoleChoices
from .models import SubBoardUser

class IsAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        role = SubBoardUser.objects.get(user=request.user).role
        return request.user.is_authenticated and role == RoleChoices.ADMIN
    
class IsViewer(BasePermission):
    def has_object_permission(self, request, view, obj):
        role = SubBoardUser.objects.get(user=request.user).role
        return request.user.is_authenticated and role == RoleChoices.VIEWER

class IsUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        role = SubBoardUser.objects.get(user=request.user).role
        return request.user.is_authenticated and role == RoleChoices.USER