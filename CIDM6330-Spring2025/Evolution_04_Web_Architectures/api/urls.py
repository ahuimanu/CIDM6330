from django.urls import include, path
from rest_framework import routers

from .views import AuthorViewSet, BookViewSet, PublisherViewSet, ReaderViewSet

router = routers.DefaultRouter()
router.register(r"books", BookViewSet)
router.register(r"authors", AuthorViewSet)
router.register(r"publishers", PublisherViewSet)
router.register(r"readers", ReaderViewSet)

app_name = "api"

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", include(router.urls)),
]
