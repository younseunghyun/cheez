from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import RelatedField
from users.models import User
from users.models import Device
from users.models import SNSAccount


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

    class Meta:
        model = User
        exclude = ('user_permissions', 'groups',)
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }

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
            device = Device(**device_data)
            device.save()

        # create sns accounts
        for sns_account_data in sns_accounts_data:
            sns_account_data['user_id'] = user.id
            sns_account = SNSAccount(**sns_account_data)
            sns_account.save()

        return user
