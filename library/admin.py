from django.contrib import admin
from .models import Library, BookAvailability

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'latitude', 'longitude', 'id')
    search_fields = ('name', 'address')

@admin.register(BookAvailability)
class BookAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('library', 'book', 'quantity', 'available', 'price', 'penalty_price', 'id')
    list_filter = ('library', 'book')
    search_fields = ('library__name', 'book__title')
