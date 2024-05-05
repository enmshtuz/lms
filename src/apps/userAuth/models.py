from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import uuid


class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)
    is_opened = models.BooleanField(default=False)

    def __str__(self):
        return f"Verification token for {self.user.username}"


class PasswordReset(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return f"Password reset token for {self.user.email}"


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
    invitation_link_expiration_days = models.IntegerField(default=3)
    verification_link_expiration_hours = models.IntegerField(default=5)


class InvitationLink(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('expired', 'Expired'),
    ]

    email = models.EmailField()
    link = models.CharField(max_length=100, unique=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"InvitationLink - {self.email} ({self.status})"

    def save(self, *args, **kwargs):
        if len(self.link) > self._meta.get_field('link').max_length:
            self.link = self.link[:self._meta.get_field('link').max_length]

        super().save(*args, **kwargs)


class Role:
    USER = 'User'
    MANAGER = 'Manager'
    ADMIN = 'Admin'

    @classmethod
    def choices(cls):
        return (
            (cls.USER, 'User'),
            (cls.MANAGER, 'Manager'),
            (cls.ADMIN, 'Admin'),
        )
