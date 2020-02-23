from rest_framework import serializers

from joke.models import Joke


class JokeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joke
        fields = ('joke', 'author', 'score', 'date')
