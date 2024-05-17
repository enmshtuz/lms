from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Course(models.Model):
    BEGINNER = 'Beginner'
    INTERMEDIATE = 'Intermediate'
    ADVANCED = 'Advanced'

    LEVEL_CHOICES = [
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    publish_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)
    file = models.FileField(upload_to='course_files/', null=True, blank=True)
    video = models.FileField(upload_to='course_videos/', null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    def publish(self):
        self.is_published = True
        self.published_date = timezone.now()
        self.save()

    def unpublish(self):
        self.is_published = False
        self.published_date = None
        self.save()

    def __str__(self):
        return self.title

    def calculate_enrolled_count(self):
        return self.enrollment_set.count()


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_forced_enrollment = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'course')


class Resource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    meta = models.CharField(max_length=100)


class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

