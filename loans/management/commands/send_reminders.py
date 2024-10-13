from django.core.management.base import BaseCommand
from loans.tasks import send_return_reminders

class Command(BaseCommand):
    help = 'Manually send return reminders'

    def handle(self, *args, **options):
        result = send_return_reminders.delay()
        self.stdout.write(self.style.SUCCESS(f'Task sent: {result}'))

