from django.urls import path
from joke import views


urlpatterns = [
    path('judge/', views.joke_judge),
    path('evaluate/', views.joke_evaluate),
]
