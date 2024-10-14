from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from library.views import LibraryViewSet, BookAvailabilityViewSet
from . import consumers

router = DefaultRouter()
router.register(r'libraries', LibraryViewSet)
router.register(r'book-availabilities', BookAvailabilityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


websocket_urlpatterns = [
    re_path(r'ws/book_availability/(?P<book_id>\d+)/$', consumers.BookAvailabilityConsumer.as_asgi()),
]

