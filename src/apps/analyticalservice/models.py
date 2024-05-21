from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


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
    publish_date = models.DateTimeField(null=True, blank=True)
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



class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(default=timezone.now)
    is_forced_enrollment = models.BooleanField(default=False)
    completed_course = models.BooleanField(default=False) 
    completion_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'course')

    def save(self, *args, **kwargs):
        if self.completed_course and not self.completion_date:
            self.completion_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"


        
class Badge(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.name



# Other course fields
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"Feedback for {self.course.title} by {self.user.username}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Resource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    meta = models.CharField(max_length=100)

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    """
    def __str__(self):
        return f"Progress for {self.user.username} in {self.enrollment.course.title}"
    """