from rest_framework.test import APILiveServerTestCase
from users.user import (
    Device,
    SNSAccount,
    User,
)

class BaseTestCase(APILiveServerTestCase):
    def setUp(self):
        self.create_users()
        self.create_posts()




    def create_users(self):
        prev_user_count = User.objects.count()

        # create user with email password
        user = User(
            email='s_polaris@naver.com',
        )
        user.set_password('some_password')
        user.save()

        self.assertEqual(prev_user_count+1, User.objects.count())




    def create_posts(self):
        pass


