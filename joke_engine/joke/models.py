from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Joke(models.Model):
    ## -----*----- Joke Model -----*----- ##

    # joke  ：ダジャレ１文
    # author：人物名（NULL許容）
    # score ：スコア（0.0~100.0）
    # date  ：作成日（変更不可）

    joke = models.CharField(
        max_length=100
    )
    author = models.CharField(
        max_length=100,
        null=True
    )
    score = models.FloatField(
        default=0,
        validators=[MinValueValidator(0.0),
                    MaxValueValidator(100.0)]
    )
    date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.joke

