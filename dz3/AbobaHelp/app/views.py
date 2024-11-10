from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from app import models


def paginate(objects, request: HttpRequest, per_page=10):
    p = Paginator(objects, per_page)
    try:
        return p.page(request.GET.get("page", 1))
    except PageNotAnInteger:
        return p.page(1)
    except EmptyPage:
        return p.page(1)
    


# Create your views here.
def index(request):
    questions = models.Question.objects.newest()
    page = paginate(questions, request)
    return render(request, "index.html", context={
        "title": "New questions:",
        "questions": page.object_list,
        "page": page
    })


def hot(request):
    questions = models.Question.objects.best()
    page = paginate(questions, request)
    return render(request, "hot.html", context={
        "questions": page.object_list,
        "page": page
    })


def found_questions(request, tag):
    questions = models.Question.objects.with_tag(tag)
    page = paginate(questions, request)
    return render(request, "index.html", context={
        "title": "Found questions:",
        "questions": page.object_list,
        "page": page
    })


def question_page(request, qid):
    try:
        question = models.Question.objects.get(id=qid)
    except models.Question.DoesNotExist:
        return Http404()
    answers = question.answer_set.best()
    page = paginate(answers, request)
    return render(request, "question.html", context={
        "question": question,
        "answers": page.object_list,
        "page": page
    })


def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "signup.html")


def ask(request):
    return render(request, "ask.html")