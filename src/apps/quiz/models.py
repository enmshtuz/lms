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
    attempts_allowed = models.IntegerField(default=1)
    deadline_minutes = models.IntegerField(default=1)
    success_criteria = models.IntegerField(default=100, validators=[MinValueValidator(1), MaxValueValidator(101)])
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Question(models.Model):
    objects = None
    QUIZ_TYPES = (
        ('radio', 'Radio'),
        ('checkbox', 'Checkbox'),
    )
    text = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=10, choices=QUIZ_TYPES)

    def __str__(self):
        return self.question_type


class Answer(models.Model):
    objects = None
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField()

    def __str__(self):
        return self.text


# class QuizResult(models.Model):
#     objects = None
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     submitted_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)


# class Attempt(models.Model):
#     objects = None
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
#     attempts_remaining = models.IntegerField(default=1, help_text="Range: 1-10")
#
#     def __str__(self):
#         return f"{self.user.username} - {self.quiz.title}"
