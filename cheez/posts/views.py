from django.db.models import Q
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from posts.models import Post
from posts.models import Tag
from posts.models import Report
from posts.serializers import PostSerializer
from users.serializers import UserSerializer

class PostViewSet(ModelViewSet):
    PAGE_SIZE = 20

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
        request.user.upload_count += 1
        request.user.save()

        return Response(serializer.data, status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        page = request.query_params.get('page', 1)

        query = """
            SELECT * FROM
            posts_post p
            LEFT JOIN users_user u
            on p.user_id = u.id
            left join posts_readpostrel rp
            on p.id = rp.post_id and rp.user_id = %s

            """
        params = [request.user.id, ]

        user_id = request.query_params.get('user_id')
        if user_id:
            query += 'where p.user_id = %s '
            params.append(user_id)
        else:
            query += 'where rp.id is null '
        query += ' limit %s, %s'
        params += [(int(page)-1)*PostViewSet.PAGE_SIZE, PostViewSet.PAGE_SIZE]
        posts = Post.objects.raw(query, params)

        serializer = self.serializer_class(posts, many=True)

        return Response({'results': serializer.data})


class ReadPostApiView(APIView):
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        # TODO : form validation

        link_clicked = 'link_clicked' in request.data and request.data['link_clicked']
        rating = 0 if 'rating' not in request.data else request.data['rating']
        saved = request.data['saved']
        post_ = Post.objects.get(id=request.data['post_id'])
        post_.read_by(request.user, link_clicked, rating, saved)

        return Response({'message': 'success'})

class SavedPostApiView(APIView):
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def get(self, request):
        posts = Post.objects.raw(
            """
            SELECT * FROM
            posts_post p
            LEFT JOIN users_user u
            on p.user_id = u.id
            left join posts_readpostrel rp
            on p.id = rp.post_id and rp.user_id = %s
            where rp.saved = '1'
            """,
            [request.user.id, ]
        )
        serializer = PostSerializer(posts, many=True)

        return Response({'results': serializer.data})

class ReportApiView(APIView):
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        post = Post.objects.get(id=request.data['post_id'])
        reason = request.data['reason']
        report = Report(
            post_id=post.id,
            user_id=request.user.id,
            reason=reason
        )
        post.reported_count += 1
        post.save()
        report.save()

        return Response({'message': 'success'})