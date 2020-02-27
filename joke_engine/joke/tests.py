from django.test import TestCase

# Create your tests here.

# import os
# import requests
# import json
#
# url = "http://localhost:8000/joke"
#
# headers = {'Content-type': 'application/json'}
# joke = '布団が吹っ飛んだ'
#
#
# # ダジャレ判定API
# res = requests.get(url + '/judge?joke=%s' % joke)
# res_json = json.loads(res.text)
# print('''
# ダジャレ判定
#     - ダジャレ：{}
#     - レスポンス：{}
# '''.format(joke, res_json))
#
#
# # ダジャレ評価API
# res = requests.get(url + '/evaluate?joke=%s' % joke)
# res_json = json.loads(res.text)
# print('''
# ダジャレ評価
#     - ダジャレ：{}
#     - レスポンス：{}
# '''.format(joke, res_json))
