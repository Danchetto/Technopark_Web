# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, Http404
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http.response import FileResponse, HttpResponseNotModified
from django.utils.http import http_date
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os

from django.core.wsgi import get_wsgi_application

from cgi import parse_qsl, escape

from questions.models import *


# Create your views here.
def index(request):
    questions = Question.objects.new()
    questions = paginate(questions, request)

    context = {
        'questions': questions
    }
    return render(request, 'index.html', context)




    # return render(request, 'index.html')

def hot(request):
    questions = Question.objects.hot()
    questions = paginate(questions, request)

    context = {
        'questions': questions
    }
    return render(request, 'hot.html', context)


def tag(request, tag_name):
    try:
        current_tag = Tag.objects.get(name=tag_name)
    except:

        raise Http404

    questions = Question.objects.filter(tag=current_tag)
    questions = paginate(questions, request)


    context = {
        'questions': questions,
        'tag': current_tag
    }

    return render(request, "search-by-tag.html", context)


def search(request):
    tag_name = request.POST['search']
    return tag(request, tag_name)


def ask(request):
    if not request.user.is_authenticated():
        return render(request, 'sign_up.html')
    return render(request, 'ask.html')


def question(request, question_id):
    question = Question.objects.get(id=question_id)

    context = {
        'question': question
    }

    return render(request, 'question.html', context)


def question_like(request, question_id):
    question = Question.objects.get(id=question_id)
    question.like()

    context = {
        'question': question
    }

    return redirect('index')

def question_dislike(request, question_id):
    question = Question.objects.get(id=question_id)
    question.dislike()

    context = {
        'question': question
    }

    return redirect('index')


@login_required()
def settings(request):

    return render(request, 'settings.html')



def save_question(request):

    question = Question(title = request.POST["question_name"],
                        text = request.POST['question_text'],
                        likes = 0,
                        dislikes = 0,
                        user = request.user.profile)

    question.make_tags(request)

    return redirect('index')



def make_answer(request, question_id):

    question = Question.objects.get(id=question_id)

    if request.user.is_authenticated:
        answer = Answer(text=request.POST["answer_text"],
                        user=request.user.profile,
                        question=question)

        question.answer_count += 1
        question.save()
        answer.save()

    else:
        return redirect('signup')

    return redirect(reverse('question', kwargs={'question_id':question_id}))


def sign_up(request):
    return render(request, 'sign_up.html')


def sign_up_confirm(request):
    user = User.objects.create_user(username=request.POST['login'],
                                    email=request.POST['email'],
                                    password=request.POST['password'])

    profile = Profile(user=user)
    profile.save()
    user.save()
    auth.login(request, user)

    return redirect("index")


def login(request):
    return render(request, 'login.html')


def login_confirm(request):

    login = request.POST['login']
    password = request.POST['password']
    user = auth.authenticate(username=login, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return redirect("index")

    else:
        redirect("login")

def logout_view(request):
    logout(request)
    return redirect("index")



def paginate(objects_list, request):

    paginator = Paginator(objects_list, 3)

    try:
        questions = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(1)

    return questions


def application(request):

    context = {'get_data' : request.GET,
               'post_data' : request.POST}
    return render(request, "test.html", context)