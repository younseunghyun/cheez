from rest_framework.test import APILiveServerTestCase
from users.models import (
    Device,
    SNSAccount,
    User,
)

from posts.models import (
    LikePostRel,
    Post,
    ReadPostRel,
)

class BaseTestCase(APILiveServerTestCase):
    def setUp(self):
        self.create_users()
        self.create_posts()

    def tearDown(self):
        ReadPostRel.objects.all().delete()
        LikePostRel.objects.all().delete()
        Post.objects.all().delete()
        Device.objects.all().delete()
        SNSAccount.objects.all().delete()
        User.objects.all().delete()


    def test_create_test_database(self):
        pass

    def create_users(self):
        prev_user_count = User.objects.count()

        # create user with email password
        user = User(
            email='s_polaris@naver.com',
        )
        user.set_password('sample_password')
        user.save()

        self.assertEqual(prev_user_count+1, User.objects.count())

        # create user with device id
        user = User()
        user.save()

        prev_device_count = Device.objects.count()
        device = Device(
            device_id='sample_device_id',
            user_id=user.id
        )
        device.save()

        self.assertEqual(prev_device_count+1, Device.objects.count())
        self.assertEqual(prev_user_count+2, User.objects.count())

        # create user with sns account
        user = User()
        user.save()

        prev_sns_count = SNSAccount.objects.count()
        sns_account = SNSAccount(
            sns_profile_url='https://www.fb.com/sample_sns_user_id',
            sns_type=SNSAccount.SNS_TYPE_FACEBOOK,
            sns_user_id='sample_sns_user_id',
            user_id=user.id,
        )
        sns_account.save()

        self.assertEqual(prev_user_count+3, User.objects.count())
        self.assertEqual(prev_sns_count+1, SNSAccount.objects.count())


    def create_posts(self):
        prev_post_count = Post.objects.count()

        user = User.objects.first()
        post = Post(
            source_url='https://www.youtube.com/watch?v=kaTi2r-6CEw',
            subtitle='언니 팔꿈치 검을 현!!',
            title='이상한 한자말투 배워와서 짜증나게 하는 동생 썰',
            user_id=user.id,
        )
        post.save()

        self.assertEqual(prev_post_count+1, Post.objects.count())

        # like post test
        prev_like_count = post.like_count

        post.liked_by(user.id)

        self.assertEqual(prev_like_count+1, post.like_count)

        self.assertEqual(post.like_post_rels.filter(like_type=LikePostRel.LIKE_TYPE_LIKE).count(), post.like_count)

        prev_read_count = post.read_count

        post.read_by(user.id)

        self.assertEqual(prev_read_count+1, post.read_count)
        self.assertEqual(post.read_post_rels.count(), post.read_count)



