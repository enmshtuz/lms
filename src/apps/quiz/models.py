from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    objects = None
    BEGINNER = 'Beginner'
    INTERMEDIATE = 'Intermediate'
    ADVANCED = 'Advanced'

    LEVEL_CHOICES = [
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
    ]

    title = models.CharField(max_length=100)
    complexity = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    attempts = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 4)])
    deadline = models.IntegerField(help_text="Deadline in minutes")
    success_criteria = models.IntegerField(default=100, validators=[MinValueValidator(1), MaxValueValidator(101)])
    is_published = models.BooleanField(default=False)
    attempts_allowed = models.IntegerField(default=1)
    deadline_minutes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Question(models.Model):
    objects = None
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    TYPE_CHOICES = [
        ('radio', 'Radio'),
        ('checkbox', 'Checkbox'),
    ]
    question_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return self.text


class Answer(models.Model):
    objects = None
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Attempt(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    attempts_remaining = models.IntegerField(default=1, help_text="Range: 1-10")

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"
