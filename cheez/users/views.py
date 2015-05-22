from django.db import IntegrityError
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from users.models import User, SNSAccount
from users.models import Device
from users.serializers import UserSerializer
from users.serializers import CustomAuthTokenSerializer


class AuthTokenAPIView(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

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
            user.save()
        else:
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)
