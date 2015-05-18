from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ogp.models import OG
from ogp.serializers import OGSerializer
from ogp.pyogp import PyOGP

class OGViewSet(ModelViewSet):
    queryset = OG.objects.all()
    serializer_class = OGSerializer

    def create(self, request, *args, **kwargs):
        url = request.data['url']

        data = {
            'url': url,
            'title': None,
            'author': None,
            'image': None,
            'video': None,
            'description': None,
        }
        og, created = OG.objects.get_or_create(url=url)
        if created:
            data = PyOGP().crawl(url).result
            serializer = self.serializer_class(og, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = self.serializer_class(og)

        return Response(serializer.data, status.HTTP_201_CREATED)




