from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from gcm.utils import notification_push

GCM_ERROR_MESSAGES = {'MissingRegistration': 'Check that the request contains a registration token',
                      'InvalidRegistration': 'Check the format of the registration token you pass to the server.',
                      'NotRegistered': 'The client app unregisters with GCM.',
                      'InvalidPackageName': 'Make sure the message was addressed to a registration token whose package'
                                            ' name matches the value passed in the request.',
                      'MismatchSenderId': 'A registration token is tied to a certain group of senders.',
                      'MessageTooBig': 'Check that the total size of the payload data included in a message does'
                                       ' not exceed GCM limits: 4096 bytes for most messages, or 2048 bytes in the case'
                                       ' of messages to topics or notification messages on iOS. This includes both'
                                       'the keys and the values.',
                      'InvalidDataKey': 'Check that the payload data does not contain a key (such as from ,'
                                        ' or gcm , or any value prefixed by google ) that is used internally by GCM.',
                      'InvalidTtl': 'Check that the value used in time_to_live is an integer representing a'
                                    ' duration in seconds between 0 and 2,419,200 (4 weeks).',
                      'Unavailable': 'The server couldn\'t process the request in time.',
                      'InternalServerError': 'The server encountered an error while trying to process the request.',
                      'DeviceMessageRate': 'The rate of messages to a particular device is too high.',
                      'TopicsMessageRate': 'The rate of messages to subscribers to a particular topic is too high.',
                      'InvalidParameters': 'Check Parameters sent'}

DEVICE_TYPES = (('IOS', "iOS"), ('ANDROID', "Android"))


class DeviceQuerySet(models.QuerySet):
    def send_messages(self, message=None, **kwargs):
        responses = []
        for device in self.all():
            response = device.send_message(message, **kwargs)
            responses.append((device.id, response))
        return responses


@python_2_unicode_compatible
class AbstractDevice(models.Model):
    dev_id = models.CharField(
        verbose_name=_("Device ID"), max_length=50, unique=True, )
    dev_type = models.CharField(
        verbose_name=_("Device Type"), max_length=255, choices=DEVICE_TYPES)
    reg_id = models.CharField(
        verbose_name=_("Registration ID"), max_length=255, unique=True)
    creation_date = models.DateTimeField(
        verbose_name=_("Creation date"), auto_now_add=True)
    modified_date = models.DateTimeField(
        verbose_name=_("Modified date"), auto_now=True)
    is_active = models.BooleanField(
        verbose_name=_("Is active?"), default=True)

    objects = DeviceQuerySet.as_manager()

    def __str__(self):
        return self.dev_id

    class Meta:
        abstract = True
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")
        ordering = ['-modified_date']

    def send_message(self, message=None, **kwargs):
        response = notification_push(self.dev_type, self.reg_id, message, **kwargs)
        if 'success' in response:
            return response['success']
        elif 'canonical_id' in response:
            self.reg_id = response['canonical_id']
            self.save()
            return 'Message send successfully'
        elif 'error' in response:
            if response['error'] == 'NotRegistered':
                self.mark_inactive()
                return GCM_ERROR_MESSAGES[response['error']]
            else:
                return GCM_ERROR_MESSAGES.get(response['error'], response['error'])

    def mark_inactive(self):
        self.is_active = False
        self.save()


class Device(AbstractDevice):
    pass
