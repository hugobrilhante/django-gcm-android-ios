from mock import patch

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APITestCase
from gcm import utils

User = get_user_model()
Device = utils.get_device_model()


class ApiDeviceTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', email='test@test.com')
        self.user.set_password('test')
        self.user.save()
        self.client.login(username='test', password='test')
        self.device = Device.objects.create(dev_id='123-1', dev_type='ANDROID', reg_id='123-1')

    def test_resgister_device(self):
        url = reverse('device-list')
        data = {'dev_id': '123-2', 'dev_type': 'ANDROID', 'reg_id': '123-2'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)

    def test_unresgister_device(self):
        kwargs = {'pk': 1}
        url = reverse('device-detail', kwargs=kwargs)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)


class ModelDeviceTest(TestCase):
    def setUp(self):
        self.device = Device.objects.create(dev_id='123-1', dev_type='ANDROID', reg_id='123-1')

        self.not_registered = Device.objects.create(dev_id='123-2', dev_type='ANDROID',
                                                    reg_id='fZBdS8D3a7U:APA91bEOMCWkMVR_IMirgiCPeFz2v7Ju_cLCaYyVYySa80s'
                                                           'fBaobYV360R2_1b0LtJQIrGGfdBbFiZvY1vM10voqPdljdYsFmKnyR8H8S4'
                                                           '1bdah4LiwHgZCWy5DOP9xhMIDcIFpKugZV')
        self.mismatch_sender_id = Device.objects.create(dev_id='123-3', dev_type='ANDROID',
                                                        reg_id='APA91bEOMCWkMVR_IMirgiCPeFz2v7Ju_cLCaYyVYySa80sfBaobYV360R2'
                                                               '_1b0LtJQIrGGfdBbFiZvY1vM10voqPdljdYsFmKnyR8H8S41bdah4LiwHgZC'
                                                               'Wy5DOP9xhMIDcIFpKugZV')

    def test_mark_inactive(self):
        self.device.mark_inactive()
        self.assertEqual(Device.objects.filter(is_active=False).count(), 1)

    @override_settings(GCM_ANDROID_APIKEY='AIzaSyDTOsEsbVUnm2sPVHrV2AuiBMsN9279czQ', )
    def test_send_message_error_NotRegistered_real(self):
        response = self.not_registered.send_message()
        self.assertEqual(response, 'The client app unregisters with GCM.')

    @override_settings(GCM_ANDROID_APIKEY='AIzaSyDTOsEsbVUnm2sPVHrV2AuiBMsN9279czQ')
    def test_send_message_error_MismatchSenderId_real(self):
        response = self.mismatch_sender_id.send_message()
        self.assertEqual(response, 'A registration token is tied to a certain group of senders.')

    @patch.object(Device, 'send_message')
    def test_send_message_successfully(self, mock_send_message):
        mock_send_message.return_value = 'Message send successfully'
        response = self.device.send_message()
        self.assertEqual(response, 'Message send successfully')

    @patch.object(Device, 'send_message')
    def test_send_message_error_MissingRegistration(self, mock_send_message):
        mock_send_message.return_value = 'Check that the request contains a registration token'
        response = self.device.send_message()
        self.assertEqual(response, 'Check that the request contains a registration token')

    @patch.object(Device, 'send_message')
    def test_send_message_error_InvalidRegistration(self, mock_send_message):
        mock_send_message.return_value = 'Check the format of the registration token you pass to the server.'
        response = self.device.send_message()
        self.assertEqual(response, 'Check the format of the registration token you pass to the server.')

    @patch.object(Device, 'send_message')
    def test_send_message_error_NotRegistered(self, mock_send_message):
        mock_send_message.return_value = 'The client app unregisters with GCM.'
        response = self.device.send_message()
        self.assertEqual(response, 'The client app unregisters with GCM.')

    @patch.object(Device, 'send_message')
    def test_send_message_error_InvalidPackageName(self, mock_send_message):
        mock_send_message.return_value = ('Make sure the message was addressed to a registration token whose package'
                                          ' name matches the value passed in the request.')
        response = self.device.send_message()
        self.assertEqual(response, 'Make sure the message was addressed to a registration token whose package'
                                   ' name matches the value passed in the request.')

    @patch.object(Device, 'send_message')
    def test_send_message_error_MismatchSenderId(self, mock_send_message):
        mock_send_message.return_value = 'A registration token is tied to a certain group of senders.'
        response = self.device.send_message()
        self.assertEqual(response, 'A registration token is tied to a certain group of senders.')

    @patch.object(Device, 'send_message')
    def test_send_message_error_MessageTooBig(self, mock_send_message):
        mock_send_message.return_value = ('Check that the total size of the payload data included in a message does'
                                          ' not exceed GCM limits: 4096 bytes for most messages, or 2048 bytes in the case'
                                          ' of messages to topics or notification messages on iOS. This includes both'
                                          'the keys and the values.')
        response = self.device.send_message()
        self.assertEqual(response, 'Check that the total size of the payload data included in a message does'
                                   ' not exceed GCM limits: 4096 bytes for most messages, or 2048 bytes in the case'
                                   ' of messages to topics or notification messages on iOS. This includes both'
                                   'the keys and the values.')

    @patch.object(Device, 'send_message')
    def test_send_message_error_InvalidDataKey(self, mock_send_message):
        mock_send_message.return_value = ('Check that the payload data does not contain a key (such as from ,'
                                          ' or gcm , or any value prefixed by google ) that is used internally by GCM.')
        response = self.device.send_message()
        self.assertEqual(response, 'Check that the payload data does not contain a key (such as from ,'
                                   ' or gcm , or any value prefixed by google ) that is used internally by GCM.')

    @patch.object(Device, 'send_message')
    def test_send_message_error_InvalidTtl(self, mock_send_message):
        mock_send_message.return_value = ('Check that the value used in time_to_live is an integer representing a'
                                          ' duration in seconds between 0 and 2,419,200 (4 weeks).')
        response = self.device.send_message()
        self.assertEqual(response, 'Check that the value used in time_to_live is an integer representing a'
                                   ' duration in seconds between 0 and 2,419,200 (4 weeks).')

    @patch.object(Device, 'send_message')
    def test_send_message_error_Unavailable(self, mock_send_message):
        mock_send_message.return_value = 'The server couldn\'t process the request in time.'
        response = self.device.send_message()
        self.assertEqual(response, 'The server couldn\'t process the request in time.')

    @patch.object(Device, 'send_message')
    def test_send_message_error_InternalServerError(self, mock_send_message):
        mock_send_message.return_value = 'The server encountered an error while trying to process the request.'
        response = self.device.send_message()
        self.assertEqual(response, 'The server encountered an error while trying to process the request.')

    @patch.object(Device, 'send_message')
    def test_send_message_error_DeviceMessageRate(self, mock_send_message):
        mock_send_message.return_value = 'The rate of messages to a particular device is too high.'
        response = self.device.send_message()
        self.assertEqual(response, 'The rate of messages to a particular device is too high.')

    @patch.object(Device, 'send_message')
    def test_send_message_error_TopicsMessageRate(self, mock_send_message):
        mock_send_message.return_value = 'The rate of messages to subscribers to a particular topic is too high.'
        response = self.device.send_message()
        self.assertEqual(response, 'The rate of messages to subscribers to a particular topic is too high.')

    @patch.object(Device, 'send_message')
    def test_send_message_error_InvalidParameters(self, mock_send_message):
        mock_send_message.return_value = 'Check Parameters sent'
        response = self.device.send_message()
        self.assertEqual(response, 'Check Parameters sent')


class UtilsTest(TestCase):
    def test_notification_push_real(self):
        response = utils.notification_push('ANDROID',
                                           'to',
                                           'message')
        self.assertEqual(response, {'error': '400 Client Error: Bad Request'})

    def test_get_device_model_real(self):
        response = utils.get_device_model()
        self.assertIs(response, Device)

    @patch('gcm.utils.notification_push')
    def test_notification_push_mock(self, mock_notification_push):
        mock_notification_push.return_value = 'Message send successfully'
        response = utils.notification_push('dev_type', 'to', 'message')
        self.assertEqual(response, 'Message send successfully')

    @patch('gcm.utils.get_device_model')
    def test_get_device_model_mock(self, mock_get_device_model):
        mock_get_device_model.return_value = Device
        response = utils.get_device_model()
        self.assertIs(response, Device)
