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
    # published_date = models.DateTimeField(null=True, blank=True)
    file = models.FileField(upload_to='course_files/', null=True, blank=True)
    video = models.FileField(upload_to='course_videos/', null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)

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

    # @property
    # def enrolled_users_count(self):
    #     return self.enrollment_set.count()


# class Enrollment(models.Model):
#     user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     course = models.ForeignKey('Course', on_delete=models.CASCADE)
#     enrolled_date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.user.username} enrolled in {self.course.title}"

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')