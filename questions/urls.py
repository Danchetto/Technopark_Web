
from django.conf.urls import url
from django.contrib import admin
from questions.views import AboutView

urlpatterns = [
    url(r'^about/', AboutView.as_view(), name='about'),
]
