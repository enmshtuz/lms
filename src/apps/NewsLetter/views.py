from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import News, Subscription
from .forms import NewsForm


@login_required
def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.save()
            return redirect('news_list')
    else:
        form = NewsForm()

    return render(request, 'create_news.html', {'form': form})


@login_required
def news_list(request):
    news_list = News.objects.all()
    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news_list.html', {'page_obj': page_obj})


@login_required
def subscribe(request):
    if request.method == 'POST':
        Subscription.objects.update_or_create(
            user=request.user,
            defaults={'subscribed': True}
        )
        return redirect('profile')
    return redirect('news_list')

#
# class Subscriber:
#     objects = None
#
#
# @login_required
# def submit(request):
#     if request.method == 'POST':
#         # Get the list of subscribed users' email addresses
#         subscribed_users = Subscriber.objects.all().values_list('email', flat=True)
#         # Get the latest news
#         latest_news = News.objects.filter(published=True).order_by('-created_at').first()
#         # Send the news to each subscribed user
#         for email in subscribed_users:
#             send_mail(
#                 latest_news.subject,
#                 latest_news.body,
#                 'your@example.com',  # Replace with your email address
#                 [email],
#                 fail_silently=False,
#             )
#     return redirect('news_list')


# @login_required
# def publish_news(request):
#     if request.method == 'POST':
#         # Get the latest news
#         latest_news = News.objects.filter(published=True).order_by('-created_at').first()
#         if latest_news:
#             # Get the list of subscribed users' email addresses
#             subscribers = Subscription.objects.filter(subscribed=True)
#             to_emails = [subscriber.user.email for subscriber in subscribers]
#
#             # Prepare email content
#             subject = latest_news.subject
#             html_message = render_to_string('email_template.html', {'news': latest_news})
#             plain_message = strip_tags(html_message)
#
#             # Send email to subscribers
#             send_mail(
#                 subject,
#                 plain_message,
#                 'your_email@example.com',  # Replace with your email address
#                 to_emails,
#                 html_message=html_message,
#             )
#
#             # Redirect to the news_list page after sending emails
#             return redirect('news_list')
#
#     # Handle non-POST requests (e.g., GET)
#     return redirect('news_list')

@login_required
def publish_news(request, news_id):
    if request.method == 'POST':
        # Get the news object based on the news_id
        news = News.objects.get(pk=news_id)
        if not news.published:
            news.publish()
            subscribers = Subscription.objects.filter(subscribed=True)
            subject = news.subject
            html_message = render_to_string('email_template.html', {'news': news})
            plain_message = strip_tags(html_message)
            from_email = 'your_email@example.com'  # Update with your email
            to_emails = [subscriber.user.email for subscriber in subscribers]
            send_mail(subject, plain_message, from_email, to_emails, html_message=html_message)
    return redirect('news_list')


# def publish_news(request, news_id):
#     news = News.objects.get(pk=news_id)
#     if not news.published:
#         news.publish()
#         subscribers = Subscription.objects.filter(subscribed=True)
#         subject = news.subject
#         html_message = render_to_string('email_template.html', {'news': news})
#         plain_message = strip_tags(html_message)
#         from_email = 'your_email@example.com'  # Update with your email
#         to_emails = [subscriber.user.email for subscriber in subscribers]
#         send_mail(subject, plain_message, from_email, to_emails, html_message=html_message)
#     return redirect('news_list')
