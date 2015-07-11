from django.conf import settings

GCM_DEVICE_MODEL = getattr(settings, 'GCM_DEVICE_MODEL', 'gcm.Device')

GCM_ANDROID_APIKEY = getattr(settings, 'GCM_ANDROID_APIKEY', None)

GCM_IOS_APIKEY = getattr(settings, 'GCM_IOS_APIKEY', None)
