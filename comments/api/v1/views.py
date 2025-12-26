from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from comments.api.v1.serializers import (
    CreateCommentSerializer,
    ResponseCommentSerializer,
)
from core.permissions import IsOwner
from comments.models import Comment


class CommentViewSet(GenericViewSet):
    queryset = Comment.objects.all()

    def get_permissions(self):
        if self.action in ["create"]:
            return [IsAuthenticated()]
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

    def create(self, request, slug=None):
        try:
            comment_data = request.data.get("comment", {})
            serializer = CreateCommentSerializer(
                data=comment_data,
                context={
                    "request": request,
                    "slug": slug,
                },
            )

            serializer.is_valid(raise_exception=True)
            comment = serializer.save()
            response_serializer = ResponseCommentSerializer(
                comment,
                context={"request": request},
            )

            return Response({"comment": response_serializer.data}, status=HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)
