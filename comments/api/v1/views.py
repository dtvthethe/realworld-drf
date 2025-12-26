from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
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
            comment = self.get_object()
            comment.delete()

            return Response(
                {"message": "Comment deleted successfully."}, status=HTTP_200_OK
            )
        except Http404:
            return Response({"error": "Comment not found."}, status=HTTP_404_NOT_FOUND)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": e.detail}, status=HTTP_400_BAD_REQUEST)
