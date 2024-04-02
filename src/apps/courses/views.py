from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello from Courses app!")

def new(request):
    return HttpResponse("New page from Courses app!")
# mysql,nginx,
