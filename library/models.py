from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from books.models import Book


class Library(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


    def __str__(self):
        return self.name

class BookAvailability(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='book_availabilities')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='availabilities')
    quantity = models.PositiveIntegerField(default=0)
    available = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0, "The book isn't available currently")]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    penalty_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ['library', 'book']

    def __str__(self):
        return f"{self.book.title} at {self.library.name}"
