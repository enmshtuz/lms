from django import forms

class EnrollmentForm(forms.Form):
    start_date_enrollment = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date_enrollment = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

class RatingForm(forms.Form):
    start_date_rating = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date_rating = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

class UserForm(forms.Form):
    start_date_user = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date_user = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

class CourseForm(forms.Form):
    start_date_course = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date_course = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
