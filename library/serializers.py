from rest_framework import serializers
from .models import Library, BookAvailability
from books.serializers import BookSerializer

class LibrarySerializer(serializers.ModelSerializer):
    distance = serializers.FloatField(read_only=True, required=False)

    class Meta:
        model = Library
        fields = ['id', 'name', 'address', 'latitude', 'longitude', 'distance']

class BookAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAvailability
        fields = ['id', 'library', 'book', 'quantity', 'available', 'price', 'penalty_price']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['library'] = str(instance.library)
        representation['book'] = str(instance.book)
        return representation

class BookAvailabilityDetailSerializer(serializers.ModelSerializer):
    library = LibrarySerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = BookAvailability
        fields = ['id', 'library', 'book', 'quantity', 'available', 'price', 'penalty_price']

class LibraryWithAvailabilitySerializer(serializers.ModelSerializer):
    book_availabilities = serializers.SerializerMethodField()
    distance = serializers.FloatField(read_only=True, required=False)

    class Meta:
        model = Library
        fields = ['id', 'name', 'address', 'latitude', 'longitude', 'distance', 'book_availabilities']

    def get_book_availabilities(self, obj):
        availabilities = obj.book_availabilities.all()
        return BookAvailabilitySerializer(availabilities, many=True).data
