from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    book_count = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0, message="Book count must be non-negative."),
            MaxValueValidator(3, message="Book count cannot exceed 3.")
        ]
    )

    def __str__(self):
        return f"{self.user.email} - {self.unique_id}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()