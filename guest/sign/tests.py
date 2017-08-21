from django.test import TestCase
from sign.models import Event,Guest
from django.contrib.auth.models import User


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


class LoginActionTest(TestCase):
    """测试登录"""
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')

    def test_add_admin(self):
        """测试添加用户"""
        user = User.objects.get(username='admin')
        self.assertEqual(user.username, 'admin')
        self.assertEqual(user.email, 'admin@mail.com')

    def test_login_action_username_password_null(self):
        """用户名密码为空"""
        test_data = {'username': '', 'password': ''}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username or password error!', response.content)

    def test_login_action_username_password_error(self):
        """用户名密码错误"""
        test_data = {'username': 'abc', 'password': '123'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username or password error!', response.content)

    def test_login_action_success(self):
        """登录成功"""
        test_data = {'username': 'admin', 'password': 'admin123456'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 302)


class EventManageTest(TestCase):
    """发布会管理"""

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(name='oneplus5', limit=2000, address='shanghai', status=1, start_time='2017-08-16 22:00')
        self.login_user = {'username': 'admin', 'password': 'admin123456'}

    def test_event_manage_success(self):
        """测试发布会"""
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'oneplus5', response.content)
        self.assertIn(b'shanghai', response.content)

    def test_event_manage_search_success(self):
        """测试发布会搜索"""
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/search_event/', {'name': 'oneplus5'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'oneplus5', response.content)
        self.assertIn(b'shanghai', response.content)


class GuestManageTest(TestCase):
    """嘉宾管理"""

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(id=1, name='oneplus5',limit=2000, address='shanghai',status=1, start_time='2017-08-16 22:00')
        Guest.objects.create(event_id=1, realname='jack', phone='18918955916', email='3123131@qq.com', sign=0)
        self.login_user = {'username': 'admin', 'password': 'admin123456'}

    def test_event_manage_success(self):
        """测试嘉宾信息"""
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'jack', response.content)
        self.assertIn(b'18918955916', response.content)

    def test_guest_manage_search_success(self):
        """测试嘉宾搜索"""
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/search_guest/', {'username': '18918955916'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'jack', response.content)
        self.assertIn(b'18918955916', response.content)


class SignIndexActionTest(TestCase):
    """发布会签到"""

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(id=1, name='oneplus5', limit=2000, address='shanghai', status=1,
                             start_time='2017-08-16 22:00')
        Event.objects.create(id=2, name='xiaomi5', limit=2000, address='shenzhen', status=1,
                             start_time='2017-08-16 22:00')
        Guest.objects.create(event_id=1, realname='jack', phone='18918955916', email='3123131@qq.com', sign=0)
        Guest.objects.create(event_id=2, realname='tom', phone='17602176634', email='284064123@qq.com', sign=1)
        self.login_user = {'username': 'admin', 'password': 'admin123456'}

    def test_sign_index_action_phone_null(self):
        """手机号为空"""
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/1/', {'phone': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'phone error.', response.content)

    def test_sign_index_action_phone_or_event_id_error(self):
        """手机号或者发布会id错误"""
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/2/', {'phone': '17602176634'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'event id or phone error.', response.content)

    def test_sign_index_action_user_has_sign(self):
        """用户已签到"""
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/2/', {'phone': '17602176634'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'user has sign in.', response.content)

    def test_sign_index_action_sign_success(self):
        """签到成功"""
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/1/', {'phone': '18918955916'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'sign in success!', response.content)