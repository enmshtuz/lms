# forms.py
from django import forms

class DateRangeForm(forms.Form):
    start_date_enrollment = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date_enrollment = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

"""
class top_rated_courses(Person):
  pass
"""