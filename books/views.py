from django.db.models import Count, Prefetch, Q
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Category, Book
from .serializers import AuthorSerializer, AuthorDetailSerializer, BookDetailSerializer, CategorySerializer, BookSerializer
from library.models import BookAvailability

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'bio']  

    def get_queryset(self):
        queryset = super().get_queryset()

        category_id = self.request.query_params.get('category')
        library_id = self.request.query_params.get('library')

        if category_id:
            queryset = queryset.filter(books__category_id=category_id)

        if library_id:
            queryset = queryset.filter(books__availabilities__library_id=library_id)

        queryset = queryset.annotate(
            book_count=Count('books', distinct=True)
        )

        if self.request.query_params.get('loaded'):
            book_filter = Q()
            if category_id:
                book_filter &= Q(category_id=category_id)
            if library_id:
                book_filter &= Q(availabilities__library_id=library_id)
            queryset = queryset.prefetch_related(
                Prefetch('books', queryset=Book.objects.filter(book_filter), to_attr='filtered_books')
            )

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.request.query_params.get('loaded'):
            return AuthorDetailSerializer
        return AuthorSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title']
    filterset_fields = ['category', 'author']

    def get_queryset(self):
        queryset = super().get_queryset()
        library_id = self.request.query_params.get('library')
        
        if library_id:
            queryset = queryset.filter(availabilities__library_id=library_id).distinct()
        
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BookDetailSerializer
        return BookSerializer
