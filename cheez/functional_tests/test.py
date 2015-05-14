from rest_framework.test import APILiveServerTestCase
from rest_framework.test import APIClient
from users.models import User
from users.models import Device
from users.models import SNSAccount
from posts.models import Post
from posts.models import Tag

class PostTestCase(APILiveServerTestCase):
    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        pass

    def test_create_user_and_post(self):
        prev_user_count = User.objects.count()

        response = self.client.post(
            '/user/',
            {
                "name": "user name",
                "email": "example@example.com",
                "password": "pw",
            },
            format="json"
        )
        self.assertEqual(response.status_code, 201, "Failed to create user: "+str(response.data))
        self.assertEqual(prev_user_count+1, User.objects.count())

        # create user with device
        prev_device_count = Device.objects.count()
        response = self.client.post(
            '/user/',
            {
                "devices": [{
                    "device_id": "unique_device_id",
                    "os_type": 1,
                }]
            },
            format="json"
        )
        self.assertEqual(response.status_code, 201, "Failed to create user: "+str(response.data))
        self.assertEqual(prev_user_count+2, User.objects.count())
        self.assertEqual(prev_device_count+1, Device.objects.count())

        # create user with sns account
        prev_sns_account_count = SNSAccount.objects.count()
        response = self.client.post(
            '/user/',
            {
                'sns_accounts': [{
                    'sns_user_id': 'sns_account_id',
                    'sns_type': 1,
                    'sns_profile_url': 'https://www.fb.com/sns_account_id',
                    'raw_data': '{ raw sns user data string here }'
                }]
            },
            format="json"
        )
        self.assertEqual(response.status_code, 201, "Failed to create user: "+str(response.data))
        self.assertEqual(prev_user_count+3, User.objects.count())
        self.assertEqual(prev_sns_account_count+1, SNSAccount.objects.count())

        # authenticate
        # get auth token
        response = self.client.post(
            '/api-auth-token/',
            {
                'username': 'example@example.com',
                'password': 'pw',
            }
        )
        self.assertEqual(response.status_code, 200, 'Failed to get access token: '+str(response.data))
        token = response.data['token']

        response = self.client.post(
            '/og/',
            {
                'url':'http://bttrfly.co',
            }
        )
        self.assertEqual(response.status_code, 401, str(response.data))

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(
            '/og/',
            {
                'url':'http://bttrfly.co',
            }
        )
        self.assertEqual(response.status_code, 201, str(response.data))

        self.assertEqual(response.data['title'], 'Butterfly')
        self.assertEqual(response.data['image'], 'http://bttrfly.co/static/res/img/banner.png')
        self.assertEqual(response.data['description'],
                         'Butterfly is a photo sharing app. Take a picture, and send it to someone.')

        prev_post_count = Post.objects.count()
        prev_tag_count = Tag.objects.count()
        response = self.client.post(
            '/post/',
            {
                'image_url': response.data['image'],
                'source_url': 'http://bttrfly.co',
                'subtitle': response.data['description'],
                'title': response.data['title'],
                'tags': ['사진', '안드로이드'],
            },
            format='json',
        )
        self.assertEqual(response.status_code, 201, 'failed to create post: {}'.format(str(response.data)))
        self.assertEqual(prev_post_count+1, Post.objects.count())
        self.assertEqual(prev_tag_count+2, Tag.objects.count())

        response = self.client.post(
            '/api-auth-token/',
            {
                'device': {
                    'device_id': 'unique_device_id',
                    'os_type': 1
                }
            },
            format='json',

        )
        self.assertEqual(response.status_code, 200)

