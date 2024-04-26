from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Badge(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# class Course(models.Model):
#     name = models.CharField(max_length=100)
#     badges = models.ManyToManyField(Badge, blank=True)
    # BEGINNER = 'Beginner'
    # INTERMEDIATE = 'Intermediate'
    # ADVANCED = 'Advanced'
    #
    # LEVEL_CHOICES = [
    #     (BEGINNER, 'Beginner'),
    #     (INTERMEDIATE, 'Intermediate'),
    #     (ADVANCED, 'Advanced'),
    # ]
    #
    # STATUS_CHOICES = [
    #     ('draft', 'Draft'),
    #     ('published', 'Published'),
    # ]
    #
    # title = models.CharField(max_length=255)
    # description = models.TextField()
    # level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    # publish_date = models.DateTimeField(default=timezone.now)
    # is_published = models.BooleanField(default=False)
    # # published_date = models.DateTimeField(null=True, blank=True)
    # file = models.FileField(upload_to='course_files/', null=True, blank=True)
    # video = models.FileField(upload_to='course_videos/', null=True, blank=True)
    # url = models.URLField(max_length=200, null=True, blank=True)
