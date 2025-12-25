from rest_framework.permissions import BasePermission


# trong BasePermission có 2 hàm quan trọng
# 1. has_permission: check login
# 2. has_object_permission: check quyền trên object, chỉ hoạt động khi gọi hàm get_object()
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
