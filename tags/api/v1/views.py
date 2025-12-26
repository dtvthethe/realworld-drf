from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from tags.models import Tag


class TagViewSet(GenericViewSet):
    queryset = Tag.objects.all()

    def list(self, request):
        try:
            tags = Tag.objects.all().values_list("name", flat=True)
            return Response({"tags": list(tags)}, status=HTTP_200_OK)
        except Exception as e:
            return Response(
                {"errors": str(e)},
                status=HTTP_400_BAD_REQUEST,
            )
