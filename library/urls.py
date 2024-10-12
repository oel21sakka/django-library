from django.urls import path, include
from rest_framework.routers import DefaultRouter
from library.views import LibraryViewSet, BookAvailabilityViewSet

router = DefaultRouter()
router.register(r'libraries', LibraryViewSet)
router.register(r'book-availabilities', BookAvailabilityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

