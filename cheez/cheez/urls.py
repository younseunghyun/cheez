from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from users import views as user_views
from ogp import views as og_views
from posts import views as post_views
admin.autodiscover()


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

    url(r'^saved-post/', post_views.SavedPostApiView.as_view()),
    url(r'^read-post/', post_views.ReadPostApiView.as_view()),
    url(r'^report/', post_views.ReportApiView.as_view()),


    url(r'^admin/', include(admin.site.urls)),
    ]
