from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.apps import apps

@shared_task
def send_loan_confirmation_email(user_email, book_title, return_date):
    subject = 'Loan Confirmation'
    message = f'Your loan for "{book_title}" has been confirmed. Please return the book by {return_date}.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    
    send_mail(subject, message, from_email, recipient_list)

@shared_task
def send_return_reminders():
    Loan = apps.get_model('loans', 'Loan')
    today = timezone.now().date()
    three_days_from_now = today + timezone.timedelta(days=3)
    
    loans_to_remind = Loan.objects.filter(
        return_date__lte=three_days_from_now,
        return_date__gte=today,
        actual_return_date__isnull=True
    )
    
    for loan in loans_to_remind:
        days_left = (loan.return_date.date() - today).days
        subject = f"Reminder: Book due in {days_left} day{'s' if days_left > 1 else ''}"
        message = f"Dear {loan.user.username},\n\nThis is a reminder that your borrowed book '{loan.book_availability.book.title}' is due to be returned in {days_left} day{'s' if days_left > 1 else ''}. Please ensure you return it on time to avoid any late fees.\n\nThank you for using our library service!"
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [loan.user.email],
            fail_silently=False,
        )
    
    return f"Sent reminders for {loans_to_remind.count()} loans."
