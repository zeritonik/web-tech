from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

import random

def generateQuestion(ind):
    question = {
        "img": "",
        "rating": random.randint(-5, 5),
        "qid": ind,
        "title": f"Question {ind}",
        "text": f"Question {ind} text",
        "tags": random.choices(
            ["html", "css", "js", "python", "django", "web", "vk", "go", "java"], 
            k=random.randint(2, 4)
        ),
        "answer_count": random.randint(0, 25),
    }
    question["answers"] = [generateAnswer(i) for i in range(question["answer_count"])]
    return question

def generateAnswer(ind):
    return {
        "img": "",
        "rating": random.randint(-5, 5),
        "text": f"bla " * random.randint(10, 30),
        "correct": random.choice([True, False])
    }


QUESTIONS = [generateQuestion(i) for i in range(random.randint(30, 65))]


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
    page = paginate(QUESTIONS, request)
    return render(request, "index.html", context={
        "title": "New questions:",
        "questions": page.object_list,
        "page": page
    })


def hot(request):
    page = paginate(QUESTIONS, request)
    return render(request, "hot.html", context={
        "questions": page.object_list,
        "page": page
    })


def found_questions(request, tag):
    questions = list(filter(lambda x: tag in x["tags"], QUESTIONS))
    page = paginate(questions, request)
    return render(request, "index.html", context={
        "title": "Found questions:",
        "questions": page.object_list,
        "page": page
    })


def question_page(request, qid):
    question = QUESTIONS[qid]
    page = paginate(question["answers"], request)
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