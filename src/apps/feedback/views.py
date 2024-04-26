from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm
from .models import Course

@login_required
def submit_feedback(request, course_id):
    course = Course.objects.get(pk=course_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.course = course
            feedback.save()
            return redirect('course_detail', course_id=course_id)
    else:
        form = FeedbackForm()
    return render(request, 'submit_feedback.html', {'form': form, 'course': course})
