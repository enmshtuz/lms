from datetime import timedelta
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import uuid

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return f"Verification token for {self.user.username}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        profile = Profile.objects.create(user=instance)
        profile.first_name = instance.first_name
        profile.last_name = instance.last_name
        profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


class SiteSettings(models.Model):
    open_registration = models.BooleanField(default=True)
    invitation_link_expiration = models.DurationField(default=timedelta(days=3))
    verification_link_expiration = models.DurationField(default=timedelta(hours=5))
