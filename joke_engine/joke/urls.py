from django.urls import path

from .views import JokeListView


urlpatterns = [
    path('joke/list/', JokeListView.as_view(), name='home')
]
