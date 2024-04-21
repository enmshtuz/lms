from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import uuid

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return f"Verification token for {self.user.username}"
