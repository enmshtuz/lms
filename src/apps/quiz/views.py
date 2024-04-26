from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, Answer
from .forms import QuizForm, QuestionForm, AnswerForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# def index(request):
#     return HttpResponse("Successfully deleted")


@login_required
def create_quiz(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.creator = request.user
            quiz.save()
            # Save questions and answers
            for i in range(int(request.POST.get('total_questions', 0))):
                question_text = request.POST.get('question_{}'.format(i))
                question_type = request.POST.get('question_type_{}'.format(i))
                question = Question.objects.create(quiz=quiz, text=question_text, question_type=question_type)
                for j in range(int(request.POST.get('total_answers_{}'.format(i), 0))):
                    answer_text = request.POST.get('answer_{}_{}'.format(i, j))
                    is_correct = request.POST.get('is_correct_{}_{}'.format(i, j)) == 'on'
                    Answer.objects.create(question=question, text=answer_text, is_correct=is_correct)
            return redirect('quiz_list', quiz_id=quiz.id)
    else:
        quiz_form = QuizForm()
    return render(request, 'create_quiz.html', {'quiz_form': quiz_form})


@login_required
def update_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.creator = request.user
            quiz.save()

            # Delete existing questions and answers for the quiz
            quiz.question_set.all().delete()  # Assuming 'question_set' is the related manager name

            # Save updated questions and answers
            total_questions_str = request.POST.get('total_questions', '')
            if total_questions_str.isdigit():
                total_questions = int(total_questions_str)
            else:
                total_questions = 0

            for i in range(total_questions):
                question_text = request.POST.get('question_{}'.format(i))
                question_type = request.POST.get('question_type_{}'.format(i))
                question = Question.objects.create(quiz=quiz, text=question_text, question_type=question_type)
                for j in range(int(request.POST.get('total_answers_{}'.format(i), 0))):
                    answer_text = request.POST.get('answer_{}_{}'.format(i, j))
                    is_correct = request.POST.get('is_correct_{}_{}'.format(i, j)) == 'on'
                    Answer.objects.create(question=question, text=answer_text, is_correct=is_correct)

            return redirect('quiz_detail', quiz_id=quiz.id)
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'update_quiz.html', {'form': form, 'quiz': quiz})


@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    paginator = Paginator(quizzes, 10)  # Assuming you want 10 quizzes per page
    page_number = request.GET.get('page')  # Corrected 'GET' attribute
    page_obj = paginator.get_page(page_number)
    return render(request, 'quiz_list.html', {'page_obj': page_obj})


def quiz_delete(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    if request.method == 'POST':
        quiz.delete()
        return redirect('quiz_list')
    return render(request, 'quiz_confirm_delete.html', {'quiz': quiz})


def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()  # Accessing questions associated with the quiz

    return render(request, 'quiz_detail.html', {'quiz': quiz, 'questions': questions})
