from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from ...models import Article
from .serializers import CreateArticleSerializer, ResponseArticleSerializer


class ArticleViewSet(GenericViewSet):
    LIST_LIMIT_DEFAULT = 10

    queryset = Article.objects.all()
    serializer_class = CreateArticleSerializer
    # mạc định là id, thay đổi thành slug
    lookup_field = "slug"

    def create(self, request):
        try:
            article_data = request.data.get("article", {})
            serializer = self.get_serializer(data=article_data)
            serializer.is_valid(raise_exception=True)
            article = serializer.save()
            response_serializer = ResponseArticleSerializer(article)

            return Response({"article": response_serializer.data}, status=HTTP_200_OK)
        except Exception as e:
            return Response({"error": e.detail}, status=HTTP_400_BAD_REQUEST)

    def retrieve(self, request, slug=None):
        try:
            # print("Retrieving article with slug:", slug)
            article = self.get_queryset().get(slug=slug)
            response_serializer = ResponseArticleSerializer(article)

            return Response({"article": response_serializer.data}, status=HTTP_200_OK)
            # return Response({"article": {}}, status=HTTP_200_OK)
        except Exception as e:
            return Response({"error": e.detail}, status=HTTP_400_BAD_REQUEST)

    def list(self, request):
        try:
            # all
            articles = self.get_queryset().all()

            # title
            title = request.query_params.get("title", None).strip()
            if title:
                articles = articles.filter(title__icontains=title)

            # tag
            # TODO: implement tag filter

            # author
            # TODO: implement author filter

            # favorited
            # TODO: implement favorited filter

            # pagination
            limit = int(request.query_params.get("limit", self.LIST_LIMIT_DEFAULT))
            offset = int(request.query_params.get("offset", 0))
            articles = articles[offset : offset + limit]

            response_serializer = ResponseArticleSerializer(articles, many=True)

            return Response(
                {
                    "articles": response_serializer.data,
                    "articlesCount": articles.count(),
                },
                status=HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": e.detail}, status=HTTP_400_BAD_REQUEST)
