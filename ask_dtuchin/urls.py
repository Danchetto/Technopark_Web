"""task1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import questions.views

urlpatterns = [

    url(r'^admin/', admin.site.urls, name="admin"),

    url(r'^$', questions.views.index, name="index"),
    url(r'^hot/$', questions.views.hot, name="hot"),

    url(r'^ask/$', questions.views.ask, name="ask_question"),
    url(r'^ask/save/$', questions.views.save_question, name="save_question"),

    url(r'^question/(?P<question_id>[0-9]+)$', questions.views.question, name='question'),
    url(r'^question/(?P<question_id>[0-9]+)/answer$', questions.views.make_answer, name="make_answer"),
    url(r'^question/(?P<question_id>[0-9]+)/like$', questions.views.question_like, name="like"),
    url(r'^question/(?P<question_id>[0-9]+)/dislike$', questions.views.question_dislike, name="dislike"),

    url(r'^tag/(?P<tag_name>[a-z A-Z 0-9 . _]+)$', questions.views.tag, name='tag'),
    url(r'^search$', questions.views.search, name='search'),


    url(r'^signup/$', questions.views.sign_up, name="signup"),
    url(r'^signup/confirm/$', questions.views.sign_up_confirm, name="signup_confirm"),

    url(r'^login/$', questions.views.login, name="login"),
    url(r'^login/confirm/$', questions.views.login_confirm, name="login_confirm"),

    url(r'^logout/$', questions.views.logout_view, name="logout"),

    url(r'^settings/$', questions.views.settings, name="user_settings"),

    url(r'^test/', questions.views.application, name="test"),
]
