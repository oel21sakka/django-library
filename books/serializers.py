from rest_framework import serializers
from .models import Author, Category, Book

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = str(instance.author)
        representation['category'] = str(instance.category)
        return representation
               
class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        depth = 1
        fields = ['id', 'title', 'author', 'category', 'description']
    
class AuthorSerializer(serializers.ModelSerializer):
    book_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'book_count']

class AuthorDetailSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()
    book_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'books', 'book_count']

    def get_books(self, obj):
        books = getattr(obj, 'filtered_books', obj.books.all())
        return BookAuthorSerializer(books, many=True, read_only=True).data


class BookAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        depth = 1
        fields = ['id', 'title', 'category', 'description']
