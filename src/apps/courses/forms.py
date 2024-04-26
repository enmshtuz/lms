from django import forms
from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'level', 'file', 'video', 'url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['video'].widget.attrs.update({'class': 'form-control-file'})

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        video = cleaned_data.get('video')
        url = cleaned_data.get('url')

        # Check that at least one of the fields (file, video, url) is filled out
        if not file and not video and not url:
            raise forms.ValidationError('Please upload a file, video, or enter a URL.')

        # Check that only one of the fields (file, video, url) is filled out
        fields_filled = sum(bool(field) for field in [file, video, url])
        if fields_filled > 1:
            raise forms.ValidationError('Please choose only one of file, video, or URL.')

        return cleaned_data
