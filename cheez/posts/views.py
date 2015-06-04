from django.db.models import Q
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from posts.models import Comment
from posts.models import Post
from posts.models import Tag
from posts.models import Report
from posts.serializers import PostSerializer
from posts.serializers import CommentSerializer
from posts.serializers import ReadPostRelSerializer
from posts.tasks import send_post_data
from posts.tasks import send_read_log
from rankings.models import CurrentTableNumber


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

        send_post_data.delay(serializer.data)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        page = request.query_params.get('page', 1)

        if 'user_id' in request.query_params:
            user_id = request.query_params.get('user_id')
            if not user_id:
                user_id = request.user.id

            query = """
            select * from
            posts_post p
            left join users_user u
            on p.user_id = u.id
            left join posts_readpostrel pr
            on p.id = pr.post_id and pr.user_id = %s
            where p.user_id = %s
            limit %s, %s
            """
            params = [user_id, user_id, (int(page)-1)*PostViewSet.PAGE_SIZE, PostViewSet.PAGE_SIZE]

        else:
            query = """
            call recommend_user(%s, %s)
            """
            params = [request.user.id, page]
        posts = Post.objects.raw(query, params)

        serializer = self.serializer_class(posts, many=True)

        return Response({'results': serializer.data})

class CommentViewSet(ModelViewSet):
    PAGE_SIZE = 20


    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, post_id=request.data.get('post_id'))

        return Response(serializer.data, status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        post_id = request.query_params.get('post_id')
        last_id = request.query_params.get('last_id', 0)

        query = """
            SELECT * FROM
            posts_comment c
            LEFT JOIN users_user u
            on c.user_id = u.id
            where c.post_id = %s
            """

        params = [post_id, ]

        if int(last_id) > 0:
            query += ' and c.id < %s '
            params.append(last_id)


        query += """
            order by c.id desc
            limit %s
            """
        params.append(CommentViewSet.PAGE_SIZE)


        comments = Comment.objects.raw(query, params)

        serializer = self.serializer_class(comments, many=True)

        return Response({'results': serializer.data})


class ReadPostApiView(APIView):
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        # TODO : form validation
        # TODO : SQL로 만들어서 바로 넣어버리자

        for i in range(len(request.data['data'])):
            data = request.data['data'][i]
            request.data['data'][i]['user_id'] = request.user.id
            post_ = Post.objects.get(id=data['post'])
            post_.read_by(request.user, **data)

        send_read_log.delay(request.data)

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