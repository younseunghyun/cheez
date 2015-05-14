from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from posts.models import Post
from posts.models import Tag
from posts.serializers import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id

        # create tags
        tags = []
        tag_strs = data['tags']
        for tag_str in tag_strs:
            tag, created = Tag.objects.get_or_create(name=tag_str)
            tag.post_count += 1
            tag.save()
            tags.append(tag.id)
        data['tags'] = tags

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)

