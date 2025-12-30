from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from core.permissions import IsOwner
from users.models import Following
from users.api.v1.serializers import ProfileResponseSerializer
from ...models import Article
from .serializers import (
    CreateArticleSerializer,
    ResponseArticleSerializer,
    UpdateArticleSerializer,
)
from ...constants import LIST_LIMIT_DEFAULT


class ArticleViewSet(GenericViewSet):
    queryset = Article.objects.all()
    # serializer_class = CreateArticleSerializer

    # mạc định là id, thay đổi thành slug
    lookup_field = "slug"

    # nếu chỉ có vài action cần verify token thì override hàm này
    def get_permissions(self):
        if self.action in ["retrieve", "list"]:
            return [AllowAny()]
        if self.action in ["update", "destroy"]:
            return [IsOwner()]
        return super().get_permissions()

    def create(self, request):
        try:
            article_data = request.data.get("article", {})
            # serializer = self.get_serializer(data=article_data)
            serializer = CreateArticleSerializer(
                data=article_data,
                context={
                    "request": request
                },  # truyền request vào context để sử dụng trong serializer
            )
            serializer.is_valid(raise_exception=True)
            article = serializer.save()
            response_serializer = ResponseArticleSerializer(
                article, context={"request": request}
            )

            return Response({"article": response_serializer.data}, status=HTTP_200_OK)
        except Exception as e:
            return Response({"error": e.detail}, status=HTTP_400_BAD_REQUEST)

    def retrieve(self, request, slug=None):
        try:
            # print("Retrieving article with slug:", slug)
            article = self.get_queryset().get(slug=slug)
            response_serializer = ResponseArticleSerializer(
                article, context={"request": request}
            )

            return Response({"article": response_serializer.data}, status=HTTP_200_OK)
            # return Response({"article": {}}, status=HTTP_200_OK)
        except Exception as e:
            if isinstance(e, APIException):
                return Response({"error": e.detail}, status=e.status_code)

            return Response(
                {"error": "An unexpected error occurred."}, status=HTTP_400_BAD_REQUEST
            )

    def list(self, request):
        try:
            # all
            articles = self.get_queryset().all()

            # title
            title = request.query_params.get("title", "").strip()
            if title:
                articles = articles.filter(title__icontains=title)

            # tag
            # TODO: implement tag filter

            # author
            # TODO: implement author filter

            # favorited
            # TODO: implement favorited filter

            # pagination
            limit = int(request.query_params.get("limit", LIST_LIMIT_DEFAULT))
            offset = int(request.query_params.get("offset", 0))
            articles = articles[offset : offset + limit]

            response_serializer = ResponseArticleSerializer(
                articles, many=True, context={"request": request}
            )

            return Response(
                {
                    "articles": response_serializer.data,
                    "articlesCount": articles.count(),
                },
                status=HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": e.detail}, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug=None):
        try:
            # article = self.get_queryset().get(slug=slug)
            # Vì trong  get_object() gọi đến has_object_permission()
            article = self.get_object()
            article.delete()

            return Response(
                {"message": "Article deleted successfully."}, status=HTTP_200_OK
            )
        except Exception as e:
            if isinstance(e, APIException):
                return Response({"error": e.detail}, status=e.status_code)

            return Response(
                {"error": "An unexpected error occurred."}, status=HTTP_400_BAD_REQUEST
            )

    def update(self, request, slug=None):
        try:
            article = self.get_object()
            article_data = request.data.get("article", {})
            serializer = UpdateArticleSerializer(
                article,
                data=article_data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            article = serializer.save()
            response_serializer = ResponseArticleSerializer(
                article, context={"request": request}
            )

            return Response({"article": response_serializer.data}, status=HTTP_200_OK)
        except Exception as e:
            if isinstance(e, APIException):
                return Response({"error": e.detail}, status=e.status_code)

            return Response(
                {"error": "An unexpected error occurred."}, status=HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["post"])
    def favorite(self, request, slug=None):
        try:
            article = self.get_object()
            user = request.user

            if article.favorites.filter(id=user.id).exists():
                return Response(
                    {"warning": "User has already favorited this article."},
                    status=HTTP_200_OK,
                )

            article.favorites.add(user)
            article.save()
            response_serializer = ProfileResponseSerializer(
                user, context={"request": request}
            )

            return Response({"profile": response_serializer.data}, status=HTTP_200_OK)
        except Exception as e:
            if isinstance(e, APIException):
                return Response({"error": e.detail}, status=e.status_code)

            return Response(
                {"error": "An unexpected error occurred."}, status=HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["delete"])
    def unfavorite(self, request, slug=None):
        try:
            article = self.get_object()
            user = request.user

            if not article.favorites.filter(id=user.id).exists():
                return Response(
                    {"warning": "User has not favorited this article yet."},
                    status=HTTP_200_OK,
                )

            article.favorites.remove(user)
            article.save()
            response_serializer = ProfileResponseSerializer(
                user, context={"request": request}
            )

            return Response(
                {"profile": response_serializer.data},
                status=HTTP_200_OK,
            )
        except Exception as e:
            if isinstance(e, APIException):
                return Response({"error": e.detail}, status=e.status_code)

            return Response(
                {"error": "An unexpected error occurred."}, status=HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["get"])
    def feed(self, request):
        try:
            user = request.user
            user_following_ids = Following.objects.filter(follower=user).values_list(
                "followee_id", flat=True
            )
            articles = (
                self.get_queryset()
                .filter(author_id__in=list(user_following_ids))
                .order_by("-created_at")
            )

            # pagination
            limit = int(request.query_params.get("limit", LIST_LIMIT_DEFAULT))
            offset = int(request.query_params.get("offset", 0))
            articles = articles[offset : offset + limit]

            response_serializer = ResponseArticleSerializer(
                articles, many=True, context={"request": request}
            )

            return Response(
                {
                    "articles": response_serializer.data,
                    "articlesCount": articles.count(),
                },
                status=HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": e.detail}, status=HTTP_400_BAD_REQUEST)
