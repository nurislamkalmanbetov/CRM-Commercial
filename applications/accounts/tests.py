from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class IwexTestCase(TestCase):

    def test_user_create(self):
        User.objects.create_user(email='test@test.asd', password='Qwerty123')
        self.assertEqual(User.objects.get(id=1).email, 'test@test.asd')
