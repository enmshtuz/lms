from django import forms
from .models import Badge


class BadgeForm(forms.ModelForm):
    class Meta:
        model = Badge
        fields = ['name', 'color']

# class CourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = ['name', 'badges']
#         widgets = {
#             'badges': forms.SelectMultiple(attrs={'class': 'form-control'})
#         }
