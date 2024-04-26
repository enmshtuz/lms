from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    objects = None
    COMPLEXITY_CHOICES = (
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    )
    title = models.CharField(max_length=100)
    complexity = models.CharField(max_length=20, choices=COMPLEXITY_CHOICES)
    attempts = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 4)])
    deadline = models.IntegerField(help_text="Deadline in minutes")
    success_criteria = models.IntegerField(default=100, choices=[(i, i) for i in range(1, 101)])
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    objects = None
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    question_type_choices = [
        ('radio', 'Radio'),
        ('checkbox', 'Checkbox')
    ]
    question_type = models.CharField(max_length=20, choices=question_type_choices)

    def __str__(self):
        return self.text


class Answer(models.Model):
    objects = None
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text