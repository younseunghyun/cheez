from django.core.urlresolvers import resolve
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .views import *


class UserViewTest(TestCase):
    def test_prevent_no_authenticated_user(self):
        factory = APIRequestFactory()
        request = factory.get('/users/', format='json')
        view = UserViewSet.as_view({'get':'list'})
        response = view(request)

        self.assertEqual(response.status_code, 403)