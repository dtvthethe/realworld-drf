from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


# trong BasePermission có 2 hàm quan trọng
# 1. has_permission: check login
# 2. has_object_permission: check quyền trên object, chỉ hoạt động khi gọi hàm get_object()
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        print("111111")
        if obj.author != request.user:
            raise PermissionDenied("You are not the owner of this object.")
        return True


class IsNotOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            raise PermissionDenied("You cannot follow/unfollow yourself.")
        return True


class IsCommentOwner(BasePermission):
    def has_permission(self, request, view):
        print("222222")

        return True
    
    def has_object_permission(self, request, view, obj):
        print(obj.author, request.user)
        if obj.author != request.user:
            raise PermissionDenied("You are not the owner of this comment.")
        return True
