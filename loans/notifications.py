from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save

def notify_book_availability(book_title):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "book_availability",
        {
            "type": "book_available",
            "message": f"Book '{book_title}' is now available!"
        }
    )