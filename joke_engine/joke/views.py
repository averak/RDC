from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework import generics
from rest_framework import viewsets
import json


def joke_judge(request):
    ## -----*----- ダジャレかどうか判定 -----*----- ##
    '''
    method：GET
    query：
        sentence: String,
    response：
        {
            is_joke: Boolean
        }
    '''

    if request.method == 'POST':
        return JsonResponse({})

    # パラメータを辞書で取得
    params = request.GET
    print(params)

    ret = {'is_joke': True}
    return JsonResponse(ret)
