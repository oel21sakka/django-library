from django_filters import rest_framework as filters
from .models import Loan
from django.utils import timezone

class LoanFilter(filters.FilterSet):
    status = filters.CharFilter(method='filter_by_status')

    class Meta:
        model = Loan
        fields = ['user', 'book_availability', 'borrow_date', 'return_date', 'actual_return_date']

    def filter_by_status(self, queryset, name, value):
        if value == 'Returned':
            return queryset.filter(actual_return_date__isnull=False)
        elif value == 'Overdue':
            return queryset.filter(actual_return_date__isnull=True, return_date__lt=timezone.now())
        elif value == 'Active':
            return queryset.filter(actual_return_date__isnull=True, return_date__gte=timezone.now())
        return queryset

