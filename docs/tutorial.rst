Tutorial
========


============
Installation
============

Install o django-gcm-android-ios::

    pip install django-gcm-android-ios

=============
Configuration
=============

Configure django-gcm-android-ios in your settings.py file::

    INSTALLED_APPS = (
         ...
        'gcm',
    )


    GCM_DEVICE_MODEL = "<model.device>" # default gcm.Device
    GCM_IOS_APIKEY = "<IOS_APIKEY>"
    GCM_ANDROID_APIKEY = "<ANDROID_APIKEY>"

Add django-gcm-android-ios resources to your URL router::

    from gcm.routers import router
    urlpatterns = [
        ...
        url(r'api/', include(router.urls)),
    ]

You can easily test if the endpoint is working by doing the following in your terminal

Register::

     curl -X POST -H "Content-Type: application/json" -H "Authorization: " -d '{
        "dev_id": "Device id",
        "dev_type": "ANDROID or IOS",
        "reg_id": "Register id"
      }' 'http://localhost:8001/api/devices'

Unregister::


     curl -X DELETE -H "Content-Type: application/json" -H "Authorization: "
     'http://localhost:8001/api/devices/<id_device>'

.. _Django Rest Framework: http://www.django-rest-framework.org/api-guide/authentication/

.. note:: Authorization, see `Django Rest Framework`_  docs.
================
Sending messages
================
Using ``Django orm``::

    from gcm.utils import get_device_model
    Device = get_device_model()

    device = Device.objects.get(dev_id=<dev_id>)

    device.send_message('my test message', collapse_key='something')

``collapse_key`` parameter is optional (default message).

If you want to send additional arguments like ``delay_while_idle`` or other, add them as named variables::

    device.send_message('my test message', delay_while_idle=True, time_to_live=5)

.. _GCM Connection Server Reference: https://developers.google.com/cloud-messaging/server-ref

.. note:: For more information, see `GCM Connection Server Reference`_  docs.

Multicast message

``django-gcm-android-ios`` supports sending message to multiple devices at once::

    from gcm.utils import get_device_model
    Device = get_device_model()
    
    Device.objects.all().send_messages('my message')

    Device.objects.filter(is_active=True).send_messages('my message', collapse_key='something')

Payload

``django-gcm-android-ios`` supports sending payload::

    from gcm.utils import get_device_model
    Device = get_device_model()

    device = Device.objects.get(dev_id=<dev_id>)

    device.send_message(data={ "score": "4x8", "time": "15:16.2342" }, collapse_key='something', time_to_live= 108)

