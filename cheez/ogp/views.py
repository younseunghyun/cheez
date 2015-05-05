from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ogp.models import OG
from ogp.serializers import OGSerializer

class OGViewSet(ModelViewSet):
    queryset = OG.objects.all()
    serializer_class = OGSerializer

    def create(self, request, *args, **kwargs):
        url = request.data['url']

        # TODO : get og data
        data = {
            'url': url,
            'title': None,
            'author': None,
            'image_url': None,
            'video_url': None,
            'description': None,
        }

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)




