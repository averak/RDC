from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework import generics
from rest_framework import viewsets
import json
import engine


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

    ret = {'is_joke': engine.is_joke(params['joke'])}
    return JsonResponse(ret)



def joke_evaluate(request):
    ## -----*----- ダジャレを評価 -----*----- ##
    # 1.0 ~ 5.0で評価する
    '''
    uri：
        /joke/evaluate
    method：
        GET
    headers：
        'Content-Type':'application/json'
    query：
        joke: String,
    response：
        {
            score: Number
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


    # =======================================

    # =======================================


    ret = {'score': 5.0}
    return JsonResponse(ret)
