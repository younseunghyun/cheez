from django.conf.urls import url, include
from rest_framework import routers
from users import views as user_views
from ogp import views as og_views
from posts import views as post_views
from rest_framework.authtoken.views import obtain_auth_token


router = routers.DefaultRouter()
router.register(r'og', og_views.OGViewSet)
router.register(r'post', post_views.PostViewSet)
router.register(r'user', user_views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # rest api auth url
    url(r'^api-auth-token/', user_views.AuthTokenAPIView.as_view()),

    ]