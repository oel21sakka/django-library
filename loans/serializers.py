from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'user', 'book_availability', 'borrow_date', 'return_date', 'actual_return_date', 'price', 'penalty_price', 'total_price']
        read_only_fields = ['price', 'penalty_price', 'total_price']

class LoanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['user', 'book_availability', 'return_date']

