from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Quiz, Question, Answer
from .forms import QuizForm, QuestionForm, AnswerForm
from django.forms import modelformset_factory

from ..userAuth.models import UserRoles


def index(request):
    return HttpResponse("Hello")


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


@login_required
def quiz_create(request):
    if is_manager(request) or is_admin(request):
        if request.method == 'POST':
            form = QuizForm(request.POST)
            if form.is_valid():
                quiz = form.save(commit=False)
                quiz.save()
                return redirect('quiz_list')
        else:
            form = QuizForm()  # Move this line out of the else block

        return render(request, 'create_quiz.html', {'form': form})
    else:
        return render(request, 'unauthorized_access.html')


@login_required()
def create_question_and_answer(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        answer_form = AnswerForm(request.POST)
        if question_form.is_valid() and answer_form.is_valid():
            question = question_form.save()
            answer = answer_form.save(commit=False)
            # answer.question = answer
            answer.save()
            return redirect('quiz_list')
    else:
        question_form = QuestionForm()
        answer_form = AnswerForm()
    return render(request, 'create_question_and_answer.html',
                  {'question_form': question_form, 'answer_form': answer_form})


# @login_required
# def create_question(request):
#     if request.method == 'POST':
#         form = QuestionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('create_answer')
#     else:  # If request method is not POST
#         form = QuestionForm()
#     return render(request, 'create_question.html', {'form': form})
#
#
# @login_required
# def create_answer(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     if request.method == 'POST':
#         form = AnswerForm(request.POST)
#         if form.is_valid():
#             answer = form.save(commit=False)
#             answer.question = question
#             answer.save()
#             return redirect('quiz_list')
#     else:  # If request method is not POST
#         form = AnswerForm()
#     return render(request, 'create_answer.html', {'form': form, 'question': question})

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

        return redirect('quiz_list')

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

# @login_required
# def take_quiz(request, quiz_id):
#     quiz = Quiz.objects.get(id=quiz_id)
#     questions = Question.objects.filter(quiz=quiz)
#     if request.method == 'POST':
#         form = QuizResultForm(request.POST)
#         if form.is_valid():
#             user = request.user
#             submitted_answers = form.cleaned_data['submitted_answer']
#             for question, submitted_answers_id in zip(questions, submitted_answers):
#                 answer = Answer.objects.get(id=submitted_answers_id)
#                 is_correct = answer.is_correct
#                 quiz_result = QuizResult.objects.create(user=user, quiz=quiz, question=question,
#                                                         submitted_answer=answer, is_correct=is_correct)
#             return redirect('published_quiz_list')
#     else:
#         choices = [(answer.id, answer.text) for answer in Answer.objects.all()]
#         form = QuizResultForm(initial={'submitted_answer': [None] * len(questions)})
#     return render(request, 'take_quiz.html', {'quiz': quiz, 'questions': questions, 'form': form})
