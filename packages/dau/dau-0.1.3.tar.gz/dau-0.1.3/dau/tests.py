from django.test import TestCase
from django.contrib.auth import get_user_model
class DAUTestCase(TestCase):

    def test_default_user_object(self):
        User = get_user_model()
        users_number = User.objects.count()
        self.assertEqual(users_number,1)
