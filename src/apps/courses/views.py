import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import Course, Enrollment, Resource, Progress
from .forms import CourseForm
from django.contrib.auth import get_user
from ..userAuth.models import UserRoles



def is_manager(request):
    user = request.user
    if user.is_authenticated:
        try:
            user_role = UserRoles.objects.get(user=user)
            return user_role.role == 'manager'
        except UserRoles.DoesNotExist:
            return False
    return False

def is_admin(request):
    user = request.user
    if user.is_authenticated:
        try:
            user_role = UserRoles.objects.get(user=user)
            return user_role.role == 'admin'
        except UserRoles.DoesNotExist:
            return False
    return False

def is_user(request):
    user = request.user
    if user.is_authenticated:
        try:
            user_role = UserRoles.objects.get(user=user)
            return user_role.role == 'user'
        except UserRoles.DoesNotExist:
            return False
    return False



def course_create(request):
    if is_manager(request) or is_admin(request):
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES)
            if form.is_valid():
                # Save the course without committing to generate a primary key
                course = form.save(commit=False)
                # Save the course to commit changes to the database
                course.save()

                # Save the file, video, and URL to the Resource model
                file = form.cleaned_data.get('file')
                video = form.cleaned_data.get('video')
                url = form.cleaned_data.get('url')
                if file:
                    Resource.objects.create(course=course, type='file', meta=file.name)
                if video:
                    Resource.objects.create(course=course, type='video', meta=video.name)
                if url:
                    Resource.objects.create(course=course, type='url', meta=url)

                return redirect('course_list')
        else:
            form = CourseForm()
        return render(request, 'create_course.html', {'form': form})
    else:
        return render(request, 'unauthorized_access.html')



@login_required
def course_update(request, pk):
    if is_manager(request) or is_admin(request):
        course = get_object_or_404(Course, pk=pk)
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES, instance=course)  # Pass request.FILES here
            if form.is_valid():
                form.save()
                return redirect('course_list')
        else:
            form = CourseForm(instance=course)
        return render(request, 'update_course.html', {'form': form})
    else:
        return render(request, 'unauthorized_access.html')



@login_required
def course_list(request):
    if is_manager(request) or is_admin(request):
        courses = Course.objects.all().order_by('-id')
        for course in courses:
            enrollment = Enrollment.objects.filter(course_id=course.id)
            course.enrolled_count = len(enrollment)
        for p_course in courses:
            enrollment = Enrollment.objects.filter(course_id=p_course.id)
            p_course.is_enrolled = enrollment.exists()
        paginator = Paginator(courses, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'course_list.html', {'page_obj': page_obj})
    else:
        return render(request, 'unauthorized_access.html')

@login_required
def course_delete(request, pk):
    if is_manager(request) or is_admin(request):
        course = get_object_or_404(Course, pk=pk)
        if request.method == 'POST':
            course.delete()
            return redirect('course_list')
        return render(request, 'course_confirm_delete.html', {'course': course})
    else:
        return render(request, 'unauthorized_access.html')


@login_required
def publish_course(request, pk):
    if is_manager(request) or is_admin(request):
        course = get_object_or_404(Course, pk=pk)

        if request.method == 'POST':
            if not course.is_published:
                course.is_published = True
                course.publish_date = timezone.localtime(timezone.now()).strftime(
                    '%Y-%m-%d %H:%M:%S')  # Set the publish date
                course.save()

            # Redirect to the page where only published courses are displayed
            print("Printing courses: ", course)
            return redirect('course_list')

        context = {'course': course}
        return render(request, 'publish_confirm.html', context)
    else:
        return render(request, 'unauthorized_access.html')

@login_required
def unpublish_course(request, pk):
    if is_manager(request) or is_admin(request):
        course = get_object_or_404(Course, pk=pk)

        if request.method == 'POST':
            if course.is_published:
                course.is_published = False
                course.save()
            courses = Course.objects.all()
            paginator = Paginator(courses, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return render(request, 'course_list.html', {'page_obj': page_obj})

        context = {'course': course}
        return render(request, 'publish_confirm.html', context)
    else:
        return render(request, 'unauthorized_access.html')

# @login_required
def published_course_list(request):
    published_courses = Course.objects.filter(is_published=True).order_by("-publish_date")
    user = get_user(request)
    for p_course in published_courses:
        enrollment = Enrollment.objects.filter(course_id=p_course.id)
        p_course.is_enrolled = enrollment.exists() and enrollment.filter(user_id=user.id)
        p_course.enrolled_count = len(enrollment)
        p_course.is_forced_enrolled = enrollment.filter(user_id=user.id) and enrollment.filter(user_id=user.id)[0].is_forced_enrollment
    paginator = Paginator(published_courses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'published_course_list.html', {'page_obj': page_obj})


@login_required
def details_course_page(request, pk, users_list=[]):
    course = get_object_or_404(Course, pk=pk)
    user = get_user(request)
    if is_admin(request):
        user.role = "admin"
    if is_manager(request):
        user.role = "manager"
    if is_user(request):
        user.role = "user"
    enrollment = Enrollment.objects.filter(course_id=course.id)
    course.is_enrolled = enrollment.exists() and enrollment.filter(user_id=user.id)
    course.enrolled_count = len(enrollment)
    course.is_forced_enrolled = enrollment.filter(user_id=user.id) and enrollment.filter(user_id=user.id)[0].is_forced_enrollment
    progesses = Progress.objects.filter(enrollment__in=enrollment)
    course_resources = []
    completed_count = 0
    for progress in progesses:
        if progress.completed:
            completed_count += 1
        course_resources.insert(len(course_resources), {'progress_id':progress.id, 'completed': progress.completed, 'resource': Resource.objects.get(id=progress.resource_id)})
    print('course_resources', course_resources)
    completed_parcent = 0
    if len(course_resources) == 0:
        completed_parcent = 0
    else:
        completed_parcent = completed_count / len(course_resources) * 100
    return render(request, 'course_enrollment_details.html', {
        'course': course,
        'course_resources': course_resources,
        "completed_parcent": str(completed_parcent),
        "users_list": users_list,
        "user": user
    })


@csrf_exempt
def update_progress(request, pk):
    print('im working')
    if request.method == 'POST':
        resource_id = request.POST.get('resource_id')
        completed = request.POST.get('completed')

        try:
            progress = Progress.objects.get(id=resource_id)
            progress.completed =  True if completed == 'true' else False
            progress.save()
            return JsonResponse({'message': 'Progress updated successfully'})
        except Progress.DoesNotExist:
            return JsonResponse({'error': 'Progress not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    user = get_user(request)
    enrollment = Enrollment.objects.filter(course_id=course.id)
    course.is_enrolled = enrollment.exists() and enrollment.filter(user_id=user.id)
    course.enrolled_count = len(enrollment)
    course.is_forced_enrolled = enrollment.filter(user_id=user.id) and enrollment.filter(user_id=user.id)[0].is_forced_enrollment
    course_resourses = Resource.objects.filter(course_id=course.id)

    if request.method == 'POST':
            enrollment = Enrollment.objects.create(user=request.user, course=course)
            for res in course_resourses:
                Progress.objects.create(user=request.user, enrollment=enrollment, resource=res, completed=False)
            return redirect('details_course', pk)
    return render(request, 'enroll_confirm.html', {'course': course})


@login_required
def unenroll_course(request, pk):
    course = get_object_or_404(Course,  id=pk)

    if request.method == 'POST':
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        progresses = Progress.objects.filter(enrollment=enrollment)
        if enrollment:
            print('deleted')
            for progress in progresses:
                progress.delete()
            enrollment.delete()
        return redirect('details_course', pk)
    return render(request, 'enroll_confirm.html', {'course': course})


@login_required
def enroll_user_list(request, pk):
    course = get_object_or_404(Course, pk=pk)
    users = User.objects.all()
    user = get_user(request)
    enrollment = Enrollment.objects.filter(course_id=course.id)
    course.is_enrolled = enrollment.exists() and enrollment.filter(user_id=user.id)
    course.enrolled_count = len(enrollment)
    course.is_forced_enrolled = enrollment.filter(user_id=user.id) and enrollment.filter(user_id=user.id)[
        0].is_forced_enrollment
    progesses = Progress.objects.filter(enrollment__in=enrollment)
    course_resources = []
    completed_count = 0

    for modUser in users:
        enrollmentUsers = enrollment.filter(user_id=modUser.id)
        if len(enrollmentUsers) == 0:
            modUser.is_forced_enrollment = None
        elif enrollmentUsers[0].is_forced_enrollment == 1:
            modUser.is_forced_enrollment = True
        else:
            modUser.is_forced_enrollment = None

    for progress in progesses:
        if progress.completed:
            completed_count += 1
        course_resources.insert(len(course_resources), {'progress_id': progress.id, 'completed': progress.completed,
                                                        'resource': Resource.objects.get(id=progress.resource_id)})
    completed_parcent = 0
    if len(course_resources) == 0:
        completed_parcent = 0
    else:
        completed_parcent = completed_count / len(course_resources) * 100
    return render(request, 'course_enrollment_details.html', {
        'course': course,
        'course_resources': course_resources,
        "completed_parcent": str(completed_parcent),
        "users_list": users})


@csrf_exempt
def force_enroll(request, pk):
    if request.method == 'POST':
        checkedUsers = request.POST.get('checked_users')
        courseId = request.POST.get('courseId')
        checkedUsersJson = json.loads(checkedUsers)
        users = User.objects.all()
        uniqueCourse = Course.objects.get(id=courseId)
        for checkedUser in checkedUsersJson:
            users = users.exclude(id=checkedUser['userId'])
            course = Course.objects.filter(id=checkedUser['courseId'])
            user = User.objects.filter(id=checkedUser['userId'])
            enrollment = Enrollment.objects.filter(course_id=course[0].id).filter(user_id=user[0].id)

            if len(enrollment) == 0:
                Enrollment.objects.create(user=user[0], course=course[0], is_forced_enrollment=1)
            else:
                exising_enrollment = enrollment.first()
                exising_enrollment.is_forced_enrollment=1
                exising_enrollment.save()
        for uncheckedUser in users:
            enrollment = Enrollment.objects.filter(course_id=uniqueCourse.id).filter(user_id=uncheckedUser.id)
            if enrollment:
                exising_enrollment = enrollment.first()
                exising_enrollment.is_forced_enrollment=0
                exising_enrollment.save()
    return JsonResponse({'message': 'Progress updated successfully'})

@login_required
def my_courses_list(request):
    user = get_user(request)
    if is_user(request):
        courses = Course.objects.all().order_by('-id')
        enrollments = Enrollment.objects.filter(user_id = user.id)
        enrollmentCourseIds = []
        myCourses = []
        for enrollment in enrollments:
            enrollmentCourseIds.insert(len(enrollmentCourseIds), enrollment.course_id)
        for enrollmentCourseid in enrollmentCourseIds:
            myCourses = courses.filter(id=enrollmentCourseid)
        for course in myCourses:
            enrollment = Enrollment.objects.filter(course_id=course.id)
            course.enrolled_count = len(enrollment)
        for p_course in myCourses:
            enrollment = Enrollment.objects.filter(course_id=p_course.id)
            p_course.is_enrolled = enrollment.exists()
        paginator = Paginator(myCourses, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'course_my_courses.html', {'page_obj': page_obj})
    else:
        return render(request, 'unauthorized_access.html')