from rest_framework.serializers import ModelSerializer
from posts.models import Comment
from posts.models import Post
from posts.models import ReadPostRel
from users.serializers import UserSerializer


class ReadPostRelSerializer(ModelSerializer):

    class Meta:
        model = ReadPostRel


class PostSerializer(ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    read_post_rels = ReadPostRelSerializer(many=True, read_only=True)

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
                  'read_post_rels',
                  )
        extra_kwargs = {
            'id': {'read_only': True},
            'user_id': {'write_only': True},
            'subtitle': {'required': False},
            'image_url': {'required': False},
            'like_count': {'read_only': True},
            'link_click_count': {'read_only': True},
            'read_post_rels': {'read_only': True}
        }

class CommentSerializer(ModelSerializer):
    user = UserSerializer(many=False, read_only=True, required=False)
    post = PostSerializer(many=False, write_only=True, required=False)

    class Meta:
        model = Comment
        fields = ('id',
                  'user',
                  'post',
                  'comment',
                  'created',
                  )
        extra_kwargs = {
            'id': {'read_only': True},
            'created': {'read_only': True},
        }