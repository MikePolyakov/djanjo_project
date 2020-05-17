from .models import Place, Article, Source
from .serializers import PlaceSerializer, ArticleSerializer, SourceSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from .permissions import ReadOnly, IsAuthor


# ViewSets define the view behavior.
class ArticleViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthor | ReadOnly]
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class SourceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser | ReadOnly]
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
