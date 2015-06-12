from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.viewsets import ModelViewSet
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from users.models import User
from users.models import SNSAccount
from users.models import Device
from users.models import Follow
from users.serializers import UserSerializer
from users.serializers import CustomAuthTokenSerializer
from users.tasks import send_user_data


class AuthTokenAPIView(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

class EditProfileApiView(APIView):


    def post(self, request):
        user = request.user
        name = request.data.get('name')
        state_message = request.data.get('state_message')

        if name is not None:
            if User.objects.filter(name=name).count() > 0:
                return Response({'message': '닉네임이 이미 사용중이에요 :('}, status=status.HTTP_400_BAD_REQUEST)
            user.name = name

        user.state_message = state_message
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, content_type='application/json')

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.raw('''
        select * from users_user u
        left join users_follow f
        on u.id = f.followee_id and f.follower_id = %s
        where u.id = %s
        ''', [request.user.id, kwargs['pk']])[0]

        serializer = self.serializer_class(user)

        return Response(serializer.data)



    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        # device 데이터는 항상 있음
        device_data = request.data['devices'][0]
        devices = Device.objects.filter(device_id=device_data['device_id'],
                                        os_type=device_data['os_type'])
        if devices.count() > 0:
            device = devices.first()
            user = device.user
            serializer = self.serializer_class(user)

            if 'sns_accounts' in request.data:
                sns_account_data = request.data['sns_accounts'][0]
                sns_account_data['user_id'] = user.id
                sns_account, created = SNSAccount.objects.update_or_create(
                    sns_user_id=sns_account_data['sns_user_id'],
                    sns_type=sns_account_data['sns_type'],
                    defaults=sns_account_data
                )
                sns_account.save()
                request.data.pop('sns_accounts')

            # update user data
            request.data.pop('devices')
            for key in request.data:
                setattr(user, key, request.data.get(key))

            user.joined = True
            user.save()
        else:
            serializer.is_valid(raise_exception=True)
            serializer.save()

        send_user_data.delay(serializer.data)

        return Response(serializer.data, status.HTTP_201_CREATED)

class PostPushToken(APIView):
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = [AllowAny]

    def post(self, request):
        device = Device.objects.get(device_id=request.data['device_id'],
                                    os_type=request.data['os_type'])
        device.push_token = request.data.get('push_token')
        device.save()

        return Response({'message': 'success'})

class FollowView(APIView):
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        target_user_id = request.data.get('user_id')
        delete = request.data.get('delete')

        target_user = User.objects.get(id=target_user_id)

        follow_filter = Follow.objects.filter(followee=target_user, follower=request.user)

        if delete:
            if follow_filter.count() > 0:
                follow = follow_filter.first()
                follow.delete()

                target_user.follower_count -= 1
                request.user.followee_count -= 1

                target_user.save()
                request.user.save()
        else:
            if follow_filter.count() == 0:
                follow = Follow(
                    follower=request.user,
                    followee=target_user
                )
                target_user.follower_count += 1
                request.user.followee_count += 1

                follow.save()
                target_user.save()
                request.user.save()

        return Response({'message': 'success'})


