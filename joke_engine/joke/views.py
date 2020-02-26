from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework import generics
from rest_framework import viewsets
import json


def joke_judge(request):
    ## -----*----- ダジャレかどうか判定 -----*----- ##
    '''
    uri：
        /joke/judge
    method：
        GET
    headers：
        'Content-Type':'application/json'
    query：
        joke: String,
    response：
        {
            is_joke: Boolean
        }
    '''

    # パラメータを辞書で取得
    params = request.GET

    # GET以外でアクセス -> return {}
    if request.method != 'GET':
        return JsonResponse({})
    # クエリを指定されていない -> return {}
    if not 'joke' in params:
        return JsonResponse({})

    print(params)

    ret = {'is_joke': True}
    return JsonResponse(ret)
