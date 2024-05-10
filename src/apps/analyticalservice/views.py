from django.shortcuts import render, redirect
from django.contrib.auth import logout 
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import DateRangeForm
from django.db import models  # Import models module here
from django.db.models import Count, Avg
from .models import Course  # Make sure to import the Course model
from .models import Enrollment, Feedback
from django.contrib.auth.models import User


#top 10 courses by enrollment number
def courses_enrollment(start_date, end_date):
    courses_enrollment = Course.objects.filter(
        enrollment__enrolled_at__range=(start_date, end_date)
    ).annotate(
        enrollment_count=models.Count('enrollment')
    ).order_by(
        '-enrollment_count'
    )[:10]
    course_data = [(course.title, course.enrollment_count) for course in courses_enrollment]
    return course_data

#top 10 courses by rating
def top_rated_courses(start_date, end_date):
    top_rated_courses = Course.objects.filter(
        feedback__date__range=(start_date, end_date)
    ).annotate(
        avg_rating=Avg('feedback__rating')
    ).order_by('-avg_rating')[:10]
    
    rating = [(course.title, course.avg_rating) for course in top_rated_courses]
    return rating

#top 10 users based on their completed course level

"""

def user_courses(start_date, end_date):
    top_users = User.objects.filter(
        enrollment__completed=True,
        =(start_date, end_date)
    ).annotate(
        completed_courses_count=Count('enrollment')
    ).order_by(
        '-completed_courses_count'
    )[:10]

    user_data = [
        {
            'username': user.username,
            'completed_courses_count': user.completed_courses_count,
        }
        for user in top_users
    ]

"""

# Create your views here.
@login_required

def reports(request):
    if request.user.username == 'admin':
        start_date_enrollment = request.GET.get('start_date_enrollment')
        end_date_enrollment = request.GET.get('end_date_enrollment')
               
        start_date_rating = request.GET.get('start_date_rating')
        end_date_rating = request.GET.get('end_date_rating')
        enrollment_data = None  # Initialize enrollment_data
        rating_data= None
        context_enrollment = None
        context_rating = None
        
        if start_date_enrollment and end_date_enrollment:  # Check if both start_date_enrollment and end_date_enrollment are provided
            enrollment_data = courses_enrollment(start_date_enrollment, end_date_enrollment)
            
        
        if start_date_rating and end_date_rating:  # Check if both start_date_enrollment and end_date_enrollment are provided
            rating_data = top_rated_courses(start_date_rating, end_date_rating)
            

        context = {
            'form_enrollment': DateRangeForm(), 
            'enrollment_data': enrollment_data,
            'form_rating': DateRangeForm(),
            'rating_data': rating_data
        }
        
        return render(request, 'reports.html', context)
    
@login_required

def logoutUser(request):
    logout(request)
    return redirect("reports")

