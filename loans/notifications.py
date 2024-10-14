from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save

def notify_book_availability(book_id, message, library_name):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"book_availability_{book_id}",
        {
            'type': 'book_available',
            'message': f"{message} is now available at {library_name}."
        }
    )
