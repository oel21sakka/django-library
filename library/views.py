from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Library, BookAvailability
from .serializers import (
    LibrarySerializer, 
    BookAvailabilitySerializer, 
    BookAvailabilityDetailSerializer,
    LibraryWithAvailabilitySerializer
)
from django.db.models import F
from django.db.models.functions import ACos, Cos, Radians, Sin
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name', 'address']
    search_fields = ['name', 'address']
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LibraryWithAvailabilitySerializer
        return LibrarySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(book_availabilities__book__category=category).distinct()
        
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(book_availabilities__book__author=author).distinct()
        
        user_lat = self.request.query_params.get('latitude')
        user_lon = self.request.query_params.get('longitude')
        if user_lat and user_lon:
            user_lat = float(user_lat)
            user_lon = float(user_lon)
            queryset = queryset.annotate(
                distance=ACos(
                    Cos(Radians(user_lat)) * Cos(Radians(F('latitude'))) *
                    Cos(Radians(F('longitude')) - Radians(user_lon)) +
                    Sin(Radians(user_lat)) * Sin(Radians(F('latitude')))
                ) * 6371
            )
        
        return queryset

class BookAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = BookAvailability.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['library', 'book', 'quantity', 'available']
    search_fields = ['library__name', 'book__title']
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BookAvailabilityDetailSerializer
        return BookAvailabilitySerializer
