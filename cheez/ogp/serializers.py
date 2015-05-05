from rest_framework.serializers import ModelSerializer
from ogp.models import OG


class OGSerializer(ModelSerializer):

    class Meta:
        model = OG
