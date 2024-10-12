from django.contrib import admin
from django.utils import timezone
from .models import Loan

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'book_title', 'library', 'borrow_date', 'return_date', 'actual_return_date', 'status', 'total_price')
    list_filter = ('book_availability__library', 'borrow_date', 'return_date', 'actual_return_date')
    search_fields = ('user__username', 'book_availability__book__title', 'book_availability__library__name')
    date_hierarchy = 'borrow_date'

    def book_title(self, obj):
        return obj.book_availability.book.title
    book_title.short_description = 'Book'

    def library(self, obj):
        return obj.book_availability.library.name
    library.short_description = 'Library'

    def status(self, obj):
        if obj.actual_return_date:
            return 'Returned'
        elif obj.return_date < timezone.now():
            return 'Overdue'
        else:
            return 'Active'
    status.short_description = 'Status'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'book_availability__book', 'book_availability__library'
        )
