from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^events$', views.slack_events),
]
