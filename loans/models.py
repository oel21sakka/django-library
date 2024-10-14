from django.db import models, transaction
from django.contrib.auth import get_user_model
from library.models import BookAvailability
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .tasks import send_loan_confirmation_email
from loans.notifications import notify_book_availability

User = get_user_model()

class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    book_availability = models.ForeignKey(BookAvailability, on_delete=models.CASCADE, related_name='loans')
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()
    actual_return_date = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    penalty_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def clean_user(self):
        if self.user.profile.book_count >= 3:
            raise ValidationError({'user': "User has reached the maximum number of borrowed books."})
        return self.user

    def clean_book_availability(self):
        if self.book_availability.available <= 0:
            raise ValidationError({'book_availability': "This book is not available for borrowing."})
        return self.book_availability

    def clean_return_date(self):
        if self.return_date < timezone.now():
            raise ValidationError({'return_date': "The return date cannot be set in the past. Please choose a future date."})
        
        if not self.borrow_date:
            self.borrow_date = timezone.now()
            
        max_return_date = self.borrow_date + timedelta(days=30)
        if self.return_date > max_return_date:
            raise ValidationError({'return_date': "The return date must be within one month of the borrow date."})
        return self.return_date

    def clean(self):
        self.clean_user()
        self.clean_book_availability()
        self.clean_return_date()

    @classmethod
    @transaction.atomic
    def create_loan(cls, user, book_availability, return_date):
        loan = cls(
            user=user,
            book_availability=book_availability,
            return_date=return_date,
            price=book_availability.price,
            penalty_price=book_availability.penalty_price
        )
        loan.full_clean()
        loan.save()

        # Update user's book count
        user.profile.book_count += 1
        user.profile.save()

        # Update book availability
        book_availability.available -= 1
        book_availability.save()

        # Send confirmation email
        send_loan_confirmation_email.delay(
            loan.user.email,
            loan.book_availability.book.title,
            loan.return_date.strftime('%Y-%m-%d')
        )

        return loan

    @transaction.atomic
    def return_book(self):
        if self.actual_return_date:
            raise ValidationError("This book has already been returned.")

        self.actual_return_date = timezone.now()
        days_overdue = max(0, (self.actual_return_date - self.return_date).days)
        self.total_price = self.price + (days_overdue * self.penalty_price)
        self.save()

        # Update user's book count
        self.user.profile.book_count -= 1
        self.user.profile.save()

        # Update book availability
        self.book_availability.available += 1
        self.book_availability.save()

        if self.book_availability.available == 1:
            library_name = self.book_availability.library.name  # Assuming a related library model
            notify_book_availability(
                self.book_availability.book.id,
                self.book_availability.book.title,
                library_name
            )

    def __str__(self):
        return f"{self.user.username} - {self.book_availability.book.title}"
