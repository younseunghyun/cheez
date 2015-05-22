from django.db.models import Q
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from posts.models import Post
from posts.models import Tag
from posts.serializers import PostSerializer
from users.serializers import UserSerializer

class PostViewSet(ModelViewSet):
    PAGE_SIZE = 10

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

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
        serializer.save(user=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)

    # def list(self, request, *args, **kwargs):
    #     page = request.query_params.get('page', 1)
    #     posts = Post.objects.raw(
    #         """
    #         SELECT * FROM
    #         posts_post p
    #         LEFT JOIN users_user u
    #         on p.user_id = u.id
    #         left join posts_readpostrel rp
    #         on p.id = rp.post_id and rp.user_id = %s
    #         where rp.id is null
    #         """,
    #         [request.user.id]
    #     )
    #     serializer = self.serializer_class(posts, many=True)
    #
    #     return Response({'results': serializer.data})


class ReadPostApiView(APIView):
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        # TODO : form validation

        link_clicked = 'link_clicked' in request.data and request.data['link_clicked']
        rating = 0 if 'rating' not in request.data else request.data['rating']
        post_ = Post.objects.get(id=request.data['post_id'])
        post_.read_by(request.user, link_clicked, rating)

        return Response({'message': 'success'})


