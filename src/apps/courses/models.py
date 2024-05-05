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


# #last commented
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_forced_enrollment = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'course')


# class CourseEnrollment(models.Model):
#     class Meta:
#         db_table = 'courses_enrollment'
#
#     ENROLLMENT_TYPE_CHOICES = [
#         (0, 'Self-Enrollment'),
#         (1, 'Manager-Enrollment')
#     ]
#
#     enrolled_at = models.DateTimeField(auto_now_add=True)
#     course = models.ForeignKey('Course', related_name='enrollments', on_delete=models.CASCADE)
#     user = models.ForeignKey(User, related_name='course_enrollments', on_delete=models.CASCADE)
#     enrollment_type = models.IntegerField(choices=ENROLLMENT_TYPE_CHOICES, default=0)
#
#     @classmethod
#     def update_enrollment(cls, user, course, is_forced=False):
#         if is_forced:
#             enrollment_type = 1
#         else:
#             enrollment_type = 0
#
#         if enrollment_type == 1:
#             result = cls.objects.update_or_create(user=user, course=course, defaults={'enrollment_type': enrollment_type})
#         else:
#             # Check if the user is already enrolled, if so, don't update
#             if not cls.objects.filter(user=user, course=course).exists():
#                 result = cls.objects.create(user=user, course=course, enrollment_type=enrollment_type)
#             else:
#                 result = None
#         return result



# class CourseEnrollment(models.Model):
#     ENROLLMENT_TYPE_CHOICES = [
#         (0, 'Self-Enrollment'),
#         (1, 'Manager-Enrollment')
#     ]
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     enrollment_date = models.DateTimeField(default=timezone.now)
#     enrollment_type = models.IntegerField(choices=ENROLLMENT_TYPE_CHOICES, default=0)



    # class Meta:
    #     unique_together = ('user', 'course')

# class CourseEnrollment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     enrollment_time = models.DateTimeField(default=timezone.now)
#     is_forced_enrollment = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f"{self.user.username} enrolled in {self.course.title} at {self.enrollment_time}"
