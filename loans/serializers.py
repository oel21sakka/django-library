from rest_framework import serializers
from django.utils import timezone
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ['id', 'user', 'book_availability', 'borrow_date', 'return_date', 'actual_return_date', 'price', 'penalty_price', 'total_price', 'status']
        read_only_fields = ['price', 'penalty_price', 'total_price']

    def get_status(self, obj):
        if obj.actual_return_date:
            return 'Returned'
        elif obj.return_date < timezone.now():
            return 'Overdue'
        else:
            return 'Active'

class LoanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['user', 'book_availability', 'return_date']
