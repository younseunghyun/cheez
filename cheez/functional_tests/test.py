from rest_framework.test import APILiveServerTestCase
from rest_framework.test import APIClient
from users.models import User
from posts.models import Post
from posts.models import Tag

class PostTestCase(APILiveServerTestCase):
    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        pass

    def test_create_user_and_post(self):
        prev_user_count = User.objects.count()

        self.client.post(
            '/user/',
            {
                'name': 'user name',
                'email': 'example@example.com',
                'password': 'pw',
            }
        )
        self.assertEqual(prev_user_count+1, User.objects.count())

        # create user with device
        self.client.post(
            '/user/',
            {
                'device': {
                    'device_id': 'unique_device_id',
                    'os_type': 'ANDROID',
                }
            }
        )
        self.assertEqual(prev_user_count+2, User.objects.count())

        # create user with sns account
        self.client.post(
            '/user/',
            {
                'sns_account': {
                    'sns_user_id': 'sns_account_id',
                    'sns_type': 'facebook',
                    'sns_profile_url': 'https://www.fb.com/sns_account_id',
                    'raw_data': '{ raw sns user data string here }'
                }
            }
        )
        self.assertEqual(prev_user_count+3, User.objects.count())

        # authenticate
        # get auth token
        response = self.client.post(
            '/api-auth-token/',
            {
                'username': 'example@example.com',
                'password': 'pw',
            }
        )
        token = response.data['token']

        response = self.client.post(
            '/og/',
            {
                'url':'http://bttrfly.co',
            }
        )
        self.assertEqual(response.status_code, 401)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(
            '/og/',
            {
                'url':'http://bttrfly.co',
            }
        )
        self.assertEqual(response.data, {'title': 'Butterfly', 'image': 'http://bttrfly.co/static/res/img/banner.png', 'description': 'Butterfly is a photo sharing app. Take a picture, and send it to someone.'})

        prev_post_count = Post.objects.count()
        prev_tag_count = Tag.objects.count()
        response = self.client.post(
            '/post/',
            {
                'image': response.data['image'],
                'subtitle': response.data['description'],
                'title': response.data['title'],
                'tags': ['사진', '안드로이드'],
            }
        )
        self.assertEqual(prev_post_count+1, Post.objects.count())
        self.assertEqual(prev_tag_count+2, Tag.objects.count())

