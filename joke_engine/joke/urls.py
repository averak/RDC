from django.urls import path

from .views import JokeListView
from .views import JokeSearch


urlpatterns = [
    path('list/', JokeListView.as_view(), name='home'),
    path('search/', JokeSearch.as_view())
]
