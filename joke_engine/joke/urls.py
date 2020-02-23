from django.urls import path

from .views import JokeListView
from .views import JokeAPIView


urlpatterns = [
    path('list/', JokeListView.as_view(), name='home'),
    path('search/', JokeAPIView.as_view())
]
