from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsOwner
from comments.models import Comment


class CommentViewSet(GenericViewSet):
    queryset = Comment.objects.all()

    def get_permissions(self):
        if self.action in ["destroy"]:
            return [IsAuthenticated(), IsOwner()]
        return []

    def destroy(self, request, slug=None, pk=None):
        try:
            comment = self.get_object()  # get_object() raise Http404 nếu không tìm thấy
            comment.delete()

            return Response(
                {"message": "Comment deleted successfully."}, status=HTTP_200_OK
            )
        except Exception as e:
            if isinstance(e, APIException):
                return Response(
                    {"error": e.detail},
                    status=e.status_code,
                )

            return Response(
                {"error": "An unexpected error occurred."},
                status=HTTP_400_BAD_REQUEST,
            )
