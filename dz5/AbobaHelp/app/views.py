from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.views.decorators.http import require_GET, require_POST

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django import http
from django import urls
from django.shortcuts import render

from django.db import IntegrityError

import json

from app import models
from app import forms

from app import ajax


def validate_and_continue(request, default="/"):
    continue_url = request.GET.get("continue", default)
    try:
        urls.resolve(continue_url)
        return HttpResponseRedirect(continue_url)
    except http.Http404:
        return HttpResponseBadRequest(f"Unsafe continue url({continue_url}) <br> <a href={default}>Go to main page</a>")


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
    profile = request.user.profile if hasattr(request.user, "profile") else None
    questions = models.Question.objects.newest()
    page = paginate(questions, request)
    return render(request, "index.html", context={
        "title": "New questions:",
        "profile": profile,
        "questions": page.object_list,
        "page": page
    })


def hot(request):
    profile = request.user.profile if hasattr(request.user, "profile") else None
    questions = models.Question.objects.best()
    page = paginate(questions, request)
    return render(request, "hot.html", context={
        "profile": profile,
        "questions": page.object_list,
        "page": page
    })


def found_questions(request, tag):
    profile = request.user.profile if hasattr(request.user, "profile") else None
    questions = models.Question.objects.with_tag(tag)
    page = paginate(questions, request)
    return render(request, "index.html", context={
        "title": "Found questions:",
        "profile": profile,
        "questions": page.object_list,
        "page": page
    })


def question_page(request, qid):
    profile = request.user.profile if hasattr(request.user, "profile") else None
    try:
        question = models.Question.objects.get(id=qid)
    except models.Question.DoesNotExist:
        return Http404()
    if (request.method == "POST"):
        form = forms.AnswerQuestionForm(data=request.POST)
        if (form.is_valid()):
            form.instance.author = request.user.profile
            form.instance.question = question
            answer = form.save()

            answers = question.answer_set.best()
            page = 0
            for i, ans in enumerate(answers):
                if (ans == answer):
                    page = i // 10 + 1
                    break

            return HttpResponseRedirect(
                f"{urls.reverse("question_page", kwargs={"qid": question.id})}?page={page}#Answer-{answer.id}"
            )
    else:
        form = forms.AnswerQuestionForm()

    answers = question.answer_set.best()
    page = paginate(answers, request)
    return render(request, "question.html", context={
        "profile": profile,
        "question": question,
        "answers": page.object_list,
        "page": page,
        "form": form
    })


@login_required
def ask(request):
    if (request.method == "POST"):
        form = forms.AskQuestionForm(data=request.POST)
        if form.is_valid():
            form.instance.author = request.user.profile
            question = form.save()
            return HttpResponseRedirect(urls.reverse("question_page", kwargs={"qid": question.id}))
    else:
        form = forms.AskQuestionForm()
    return render(request, "ask.html", context={"form": form})


@login_required
def settings(request):
    if (request.method == "POST"):
        form = forms.UserSettingsForm(user=request.user, data=request.POST, files=request.FILES)
        if not form.is_valid():
            pass
        elif not form.save():
            form.add_error("__all__", "An error has oqqured, try again")
        
    else:
        form = forms.UserSettingsForm(user=request.user)
    return render(request, "settings.html", context={
        "form": forms.UserSettingsForm(user=request.user)
    })


@csrf_exempt
def login(request):
    if (request.user.is_authenticated):
        return validate_and_continue(request)
    
    if (request.method == "POST"):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, username=form.cleaned_data["login"], password=form.cleaned_data["password"])
            if (user is not None):
                auth.login(request, user)
                return validate_and_continue(request)
            else:
                form.add_error("__all__", "Invalid login or password")
    else:
        form = forms.LoginForm()
    return render(request, "login.html", context={"form": form})


@login_required
def logout(request):
    auth.logout(request)
    continue_url = request.GET.get("continue", urls.reverse("index"))
    return HttpResponseRedirect(continue_url)


@csrf_exempt
def signup(request):
    if (request.user.is_authenticated):
        return validate_and_continue(request)
    
    if (request.method == "POST"):
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            print("here", form.cleaned_data)
            user = form.save()
            if (user is not None):
                return HttpResponseRedirect(urls.reverse("index"))
            form.add_error("__all__", "An error has oqqured, try again")
    else:
        form = forms.SignupForm()
    return render(request, "signup.html", {"form": form})


@require_POST
@ajax.login_required_ajax
def like_question(request, qid):
    profile = request.user.profile
    like = json.loads(request.body).get("like", 0)
    try:
        question = models.Question.objects.get(id=qid)
        models.QuestionLike(question=question, author=profile, like=like).save()
    except IntegrityError as e:
        return ajax.AjaxHttpResponseError("inv_req", str(e))
    except models.Question.DoesNotExist:
        return ajax.AjaxHttpResponseError("inv_req", "Question not found")
    except Exception as e:
        return ajax.AjaxHttpResponseError("int_err", str(e))
    return ajax.AjaxHttpResponse(data={"rating": question.rating})


@require_POST
@ajax.login_required_ajax
def like_answer(request, aid):
    profile = request.user.profile
    like = json.loads(request.body).get("like", 0)
    try:
        answer = models.Answer.objects.get(id=aid)
        models.AnswerLike(answer=answer, author=profile, like=like).save()
    except IntegrityError as e:
        return ajax.AjaxHttpResponseError("inv_req", str(e))
    except models.Answer.DoesNotExist:
        return ajax.AjaxHttpResponseError("inv_req", "Answer not found")
    except Exception as e:
        return ajax.AjaxHttpResponseError("int_err", str(e))
    return ajax.AjaxHttpResponse(data={"rating": answer.rating})


@require_POST
@ajax.login_required_ajax
def correct_answer(request, aid):
    profile = request.user.profile
    correct = json.loads(request.body).get("correct", False)

    try:
        answer = models.Answer.objects.get(id=aid)
    except models.Answer.DoesNotExist:
        return ajax.AjaxHttpResponseError("inv_req", "Answer not found")
    
    if (profile != answer.question.author):
        return ajax.AjaxHttpResponseError("inv_req", "You are not the author of this question")
    answer.correct = correct
    answer.save()
    return ajax.AjaxHttpResponse(data={"correct": correct})