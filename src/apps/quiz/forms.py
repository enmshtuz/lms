from django import forms
from .models import Quiz, Question, Answer


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'complexity', 'attempts_allowed', 'deadline_minutes', 'success_criteria', 'attempts_allowed',
                  'deadline_minutes']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'quiz', 'question_type')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text', 'question', 'is_correct')

#
# class QuizResultForm(forms.ModelForm):
#     class Meta:
#         model = QuizResult
#         fields = ['submitted_answer', 'is_correct']

# class AttemptForm(forms.ModelForm):
#     class Meta:
#         model = Attempt
#         fields = ['attempts_remaining']
