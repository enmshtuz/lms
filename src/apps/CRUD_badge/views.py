from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Badge
from .forms import BadgeForm


@staff_member_required
def create_badge(request):
    if request.method == 'POST':
        form = BadgeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('badge_list')
    else:
        form = BadgeForm()
    return render(request, 'create_badge.html', {'form': form})


@staff_member_required
def update_badge(request, badge_id):
    badge = Badge.objects.get(pk=badge_id)
    if request.method == 'POST':
        form = BadgeForm(request.POST, instance=badge)
        if form.is_valid():
            form.save()
            return redirect('badge_list')
    else:
        form = BadgeForm(instance=badge)
    return render(request, 'update_badge.html', {'form': form})


def badge_delete(request, badge_id):
    badge = get_object_or_404(Badge, pk=badge_id)
    if request.method == 'POST':
        badge.delete()
        return redirect('badge_list')
    return render(request, 'badge_confirm_delete.html', {'badge': badge})



@login_required
def badge_list(request):
    badges = Badge.objects.all()
    paginator = Paginator(badges, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'badge_list.html', {'page_obj': page_obj})
#
# @login_required
# def create_course(request):
#     if request.method == 'POST':
#         form = CourseForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('course_list')
#     else:
#         form = CourseForm()
#     return render(request, 'create_course.html', {'form': form})
#
# @login_required
# def update_course(request, course_id):
#     course = Course.objects.get(pk=course_id)
#     if request.method == 'POST':
#         form = CourseForm(request.POST, instance=course)
#         if form.is_valid():
#             form.save()
#             return redirect('course_list')
#     else:
#         form = CourseForm(instance=course)
#     return render(request, 'update_course.html', {'form': form})

# def course_create(request):
#     if request.method == 'POST':
#         form = CourseForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('course_list')
#     else:
#         form = CourseForm()
#     return render(request, 'create_course.html', {'form': form})

# @login_required
# def course_list(request):
#     courses = Course.objects.all()
#     paginator = Paginator(courses, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'course_list.html', {'page_obj': page_obj})
