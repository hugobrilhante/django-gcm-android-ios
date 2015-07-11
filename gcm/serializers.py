from rest_framework.serializers import ModelSerializer

from gcm.utils import get_device_model

Device = get_device_model()


class DeviceSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = ('dev_id', 'dev_type', 'reg_id')
