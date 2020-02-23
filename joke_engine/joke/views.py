from django.shortcuts import render
from django.views.generic import ListView
from .models import Joke

# Create your views here.
class JokeListView(ListView):
    model = Joke
    template_name = 'joke_list.html'
