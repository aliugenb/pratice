from django.test import TestCase
from sign.models import Event,Guest

# Create your tests here.
class MoudleTest(TestCase):

    def setUp(self):
        Event.objects.create(id=1, name='oneplus5', status=True, limit=2000, address='shanghai', start_time='2017-08-16 22:00')
        Guest.objects.create(id=1, event_id=1, realname='jack', phone='18918955916', email='3123131@qq.com', sign=False)

    def test_event_models(self):
        result = Event.objects.get(name='oneplus5')
        self.assertEqual(result.address, 'shanghai')
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone=18918955916)
        self.assertEqual(result.realname, 'jack')
        self.assertFalse(result.sign)