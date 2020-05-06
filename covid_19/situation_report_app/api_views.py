from .models import Place, Article, Source
from .serializers import PlaceSerializer, ArticleSerializer, SourceSerializer
from rest_framework import viewsets


# ViewSets define the view behavior.
class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
