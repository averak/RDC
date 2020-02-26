from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView
from rest_framework import generics
from rest_framework import viewsets
from .serializers import JokeSerializer
from .models import Joke
import json


class JokeSearch(generics.ListAPIView):
    ## -----*----- Jokeを検索 -----*----- ##
    # method：GET

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

