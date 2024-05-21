from django.shortcuts import render, redirect
from django.contrib.auth import logout 
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import EnrollmentForm, RatingForm, UserForm, CourseForm
from django.db import models  
from django.db.models import Count, Avg
from .models import Course  
from .models import Enrollment, Feedback
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from datetime import date, timedelta, datetime



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
def reports(request):
    if request.user.username == 'admin':
        form_enrollment = EnrollmentForm(request.GET or None)
        form_rating = RatingForm(request.GET or None)
        form_user = UserForm(request.GET or None)
        form_course = CourseForm(request.GET or None)

        # Set default start and end dates for the last 30 days
        default_start_date = date.today() - timedelta(days=30)
        default_end_date = date.today()

        # Function to convert string to date
        def str_to_date(date_str):
            return datetime.strptime(date_str, "%Y-%m-%d").date()

        # Function to get date from form or session or default
        def get_date(form_field, session_key, default_date):
            form_value = form_field.value()
            if form_value:
                return str_to_date(form_value)
            date_str = request.session.get(session_key)
            return str_to_date(date_str) if date_str else default_date

        # Determine the start and end dates for each form
        start_date_enrollment = get_date(form_enrollment['start_date_enrollment'], 'start_date_enrollment', default_start_date)
        end_date_enrollment = get_date(form_enrollment['end_date_enrollment'], 'end_date_enrollment', default_end_date)

        start_date_rating = get_date(form_rating['start_date_rating'], 'start_date_rating', default_start_date)
        end_date_rating = get_date(form_rating['end_date_rating'], 'end_date_rating', default_end_date)

        start_date_user = get_date(form_user['start_date_user'], 'start_date_user', default_start_date)
        end_date_user = get_date(form_user['end_date_user'], 'end_date_user', default_end_date)

        start_date_course = get_date(form_course['start_date_course'], 'start_date_course', default_start_date)
        end_date_course = get_date(form_course['end_date_course'], 'end_date_course', default_end_date)

        # Generate data based on the date range
        enrollment_data = courses_enrollment(start_date_enrollment, end_date_enrollment)
        rating_data = top_rated_courses(start_date_rating, end_date_rating)
        user_data = user_completed_courses(start_date_user, end_date_user)
        course_data = courses_completed_count(start_date_course, end_date_course)

        # Save the dates as strings to the session for future requests
        request.session['enrollment_data'] = enrollment_data
        request.session['start_date_enrollment'] = start_date_enrollment.strftime("%Y-%m-%d")
        request.session['end_date_enrollment'] = end_date_enrollment.strftime("%Y-%m-%d")

        request.session['rating_data'] = rating_data
        request.session['start_date_rating'] = start_date_rating.strftime("%Y-%m-%d")
        request.session['end_date_rating'] = end_date_rating.strftime("%Y-%m-%d")

        request.session['user_data'] = user_data
        request.session['start_date_user'] = start_date_user.strftime("%Y-%m-%d")
        request.session['end_date_user'] = end_date_user.strftime("%Y-%m-%d")

        request.session['course_data'] = course_data
        request.session['start_date_course'] = start_date_course.strftime("%Y-%m-%d")
        request.session['end_date_course'] = end_date_course.strftime("%Y-%m-%d")

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
