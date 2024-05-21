from django.shortcuts import render, redirect
from django.contrib.auth import logout 
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import EnrollmentForm, RatingForm, UserForm, CourseForm
from django.db import models  # Import models module here
from django.db.models import Count, Avg
from .models import Course  # Make sure to import the Course model
from .models import Enrollment, Feedback
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from datetime import date, timedelta



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

def user_completed_courses(start_date, end_date):
    top_users = User.objects.filter(
        enrollment__completed_course=True,
        enrollment__completion_date__range=(start_date, end_date)
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
    return user_data

def courses_completed_count(start_date, end_date):
    top_courses = Course.objects.filter(
        enrollment__completed_course=True,
        enrollment__completion_date__range=(start_date, end_date)
    ).annotate(
        completed_count=Count('enrollment')
    ).order_by(
        '-completed_count'
    )[:10]

    course_data = [
        {
            'course_title': course.title,
            'completed_count': course.completed_count,
        }
        for course in top_courses
    ]
    return course_data

@login_required

# Create your views here.
def reports(request):
    if request.user.username == 'admin':
        # Initialize forms with initial values
        form_enrollment = EnrollmentForm(request.GET or None)
        form_rating = RatingForm(request.GET or None)
        form_user = UserForm(request.GET or None)
        form_course = CourseForm(request.GET or None)
        
        # Use form data or default to initial values
        start_date_enrollment = form_enrollment['start_date_enrollment'].value() or date.today() - timedelta(days=30)
        end_date_enrollment = form_enrollment['end_date_enrollment'].value() or date.today()
        start_date_rating = form_rating['start_date_rating'].value() or date.today() - timedelta(days=30)
        end_date_rating = form_rating['end_date_rating'].value() or date.today()
        start_date_user = form_user['start_date_user'].value() or date.today() - timedelta(days=30)
        end_date_user = form_user['end_date_user'].value() or date.today()
        start_date_course = form_course['start_date_course'].value() or date.today() - timedelta(days=30)
        end_date_course = form_course['end_date_course'].value() or date.today()

        # Retrieve existing session data if available
        enrollment_data = request.session.get('enrollment_data')
        rating_data = request.session.get('rating_data')
        user_data = request.session.get('user_data')
        course_data = request.session.get('course_data')

        if start_date_enrollment and end_date_enrollment:
            enrollment_data = courses_enrollment(start_date_enrollment, end_date_enrollment)
            request.session['enrollment_data'] = enrollment_data

        if start_date_rating and end_date_rating:
            rating_data = top_rated_courses(start_date_rating, end_date_rating)
            request.session['rating_data'] = rating_data

        if start_date_user and end_date_user:
            user_data = user_completed_courses(start_date_user, end_date_user)
            request.session['user_data'] = user_data

        if start_date_course and end_date_course:
            course_data = courses_completed_count(start_date_course, end_date_course)
            request.session['course_data'] = course_data

        context = {
            'form_enrollment': form_enrollment,
            'enrollment_data': enrollment_data,
            'form_rating': form_rating,
            'rating_data': rating_data,
            'form_user': form_user,
            'user_data': user_data,
            'form_course': form_course,
            'course_data': course_data
        }

        return render(request, 'reports.html', context)
    
@login_required

def logoutUser(request):
    logout(request)
    return redirect("reports")
