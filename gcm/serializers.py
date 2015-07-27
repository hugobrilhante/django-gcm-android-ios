from rest_framework.serializers import ModelSerializer

from gcm.utils import get_device_model

Device = get_device_model()


class DeviceSerializer(ModelSerializer):
    class Meta:
        model = Device
        exclude = ('id', 'creation_date', 'modified_date', 'is_active')
