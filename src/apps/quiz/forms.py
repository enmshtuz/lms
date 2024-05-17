from django import forms
from .models import Quiz, Question, Answer, Attempt


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'complexity', 'attempts', 'deadline', 'success_criteria', 'attempts_allowed', 'deadline_minutes']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'question_type')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text', 'is_correct')


class AttemptForm(forms.ModelForm):
    class Meta:
        model = Attempt
        fields = ['attempts_remaining']
