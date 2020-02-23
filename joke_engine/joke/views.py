from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import generics
from .serializers import JokeSerializer
from .models import Joke


class JokeListView(ListView):
    ## -----*----- Joke一覧を表示 -----*----- ##
    # method：GET

    model = Joke
    template_name = 'joke_list.html'


class JokeSearch(generics.ListAPIView):
    ## -----*----- Jokeを検索 -----*----- ##
    # method：GET

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer
