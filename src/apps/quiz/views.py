from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Quiz, Question, Answer, Attempt
from .forms import QuizForm, QuestionForm, AnswerForm, AttemptForm


def index(request):
    return HttpResponse("Hello")


@login_required
def quiz_create(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.save()
            return redirect('quiz_list')
    else:
        form = QuizForm()  # Move this line out of the else block

    return render(request, 'create_quiz.html', {'form': form})


@login_required
def quiz_update(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)

    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('quiz_list')
    else:
        form = QuizForm(instance=quiz)

    return render(request, 'update_quiz.html', {'form': form})


@login_required
def quiz_list(request):
    quiz = Quiz.objects.all()
    paginator = Paginator(quiz, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'quiz_list.html', {'page_obj': page_obj})


@login_required
def quiz_delete(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        quiz.delete()
        return redirect('quiz_list')
    return render(request, 'quiz_confirm_delete.html', {'quiz': quiz})


def publish_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)

    if request.method == 'POST':
        if not quiz.is_published:
            quiz.is_published = True
            quiz.publish_date = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')
            quiz.save()

        return redirect('published_quiz_list')

    context = {'quiz': quiz}
    return render(request, 'publish_confirm.html', context)


def unpublish_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)

    if request.method == 'POST':
        if quiz.is_published:
            quiz.is_published = False
            quiz.save()

        # Render the current page again with all quizzes
        quizzes = Quiz.objects.all()
        paginator = Paginator(quizzes, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'quiz_list.html', {'page_obj': page_obj})

    context = {'quiz': quiz}
    return render(request, 'publish_confirm.html', context)


def published_quiz_list(request):
    published_quiz = Quiz.objects.filter(is_published=True)
    paginator = Paginator(published_quiz, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'published_quiz_list.html', {'page_obj': page_obj})


def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    attempt = Attempt.objects.filter(user=request.user, quiz=quiz).first()
    if attempt and attempt.attempts_remaining <= 0:
        return HttpResponse("You have used all your attempts for this quiz.")

    # Check if the current time has exceeded the dealine
    if quiz.deadline_minutes and timezone.now() > quiz.publish_date + timezone.timedelta(minutes=quiz.deadline_minutes):
        return HttpResponse("The deadline for this quiz has passed. You cannot submit your answers.")

    if request.method == 'POST':
        if attempt:
            attempt.attempts_remaining -= 1
            attempt.save()
        else:
            Attempt.objects.create(user=request.user, quiz=quiz, attempts_remaining=quiz.attempts_allowed - 1)

            return redirect('quiz_list')

    else:
        form = AttemptForm(initial={'attempts_remaining': quiz.attempts_allowed})
        return render(request, 'quiz_detail.html', {'quiz': quiz, 'form': form})
