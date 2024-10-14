from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Loan
from .serializers import LoanSerializer, LoanCreateSerializer
from .filters import LoanFilter
from django.core.exceptions import ValidationError

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = LoanFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return LoanCreateSerializer
        return LoanSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            loan = Loan.create_loan(
                user=serializer.validated_data['user'],
                book_availability=serializer.validated_data['book_availability'],
                return_date=serializer.validated_data['return_date']
            )
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        headers = self.get_success_headers(serializer.data)
        return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        loan = self.get_object()
        try:
            loan.return_book()
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(LoanSerializer(loan).data)
