from rest_framework.serializers import ModelSerializer
from posts.models import Post
from users.serializers import UserSerializer


class PostSerializer(ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ('id',
                  'user',
                  'image_url',
                  'source_url',
                  'like_count',
                  'link_click_count',
                  'title',
                  'subtitle',
                  )
        extra_kwargs = {
            'id': {'read_only': True},
            'user_id': {'write_only': True},
            'subtitle': {'required': False},
            'image_url': {'required': False},
            'like_count': {'read_only': True},
            'link_click_count': {'read_only': True},
        }