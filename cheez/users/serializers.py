from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import RelatedField
from users.models import User
from users.models import Device
from users.models import SNSAccount
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import exceptions, serializers



class DeviceSerializer(ModelSerializer):

    class Meta:
        model = Device
        extra_kwargs = {
            'user': {'required': False}
        }


class SNSAccountSerializer(ModelSerializer):

    class Meta:
        model = SNSAccount
        extra_kwargs = {
            'user': {'required': False}
        }


class UserSerializer(ModelSerializer):
    devices = DeviceSerializer(many=True, write_only=True, required=False)
    sns_accounts = SNSAccountSerializer(many=True, write_only=True, required=False)

    def to_internal_value(self, data):
        devices_data = []
        if 'devices' in data:
            devices_data = data.pop('devices')

        sns_accounts_data = []
        if 'sns_accounts' in data:
            sns_accounts_data = data.pop('sns_accounts')
        data = super(UserSerializer, self).to_internal_value(data)
        data['devices'] = devices_data
        data['sns_accounts'] = sns_accounts_data
        return data


    def create(self, validated_data):
        if 'devices' in validated_data:
            devices_data = validated_data.pop('devices')
        else:
            devices_data = []

        if 'sns_accounts' in validated_data:
            sns_accounts_data = validated_data.pop('sns_accounts')
        else:
            sns_accounts_data = []

        user = User.objects.create(**validated_data)
        user.save()

        # create devices
        for device_data in devices_data:
            device_data['user_id'] = user.id
            device, created = Device.objects.update_or_create(
                device_id=device_data['device_id'],
                os_type=device_data['os_type'],
                defaults=device_data
            )
            device.save()

        # create sns accounts
        for sns_account_data in sns_accounts_data:
            sns_account_data['user_id'] = user.id
            sns_account, created = SNSAccount.objects.update_or_create(
                sns_user_id=sns_account_data['sns_user_id'],
                sns_type=sns_account_data['sns_type'],
                defaults=sns_account_data
            )
            sns_account.save()

        return user

    class Meta:
        model = User
        exclude = ('user_permissions', 'groups',)
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            }


class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(style={'input_type': 'password'}, required=False)
    device = serializers.RelatedField(queryset=Device.objects.all(), required=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        # {'device': {'device_id': ___, 'os_type': ___}}
        device = attrs.get('device')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise exceptions.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        elif device:
            device = Device.objects.get(**device)
            user = device.user
        else:
            msg = _('Must include "username" and "password" or "device".')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs

    def to_internal_value(self, data):
        return data
