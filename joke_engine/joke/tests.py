from django.test import TestCase

# Create your tests here.

import requests
import json


url = "http://localhost:8000/joke"

headers = {'Content-type': 'application/json'}
joke = '布団が吹っ飛んだ'


# ダジャレ判定API
res = requests.get(url + '/judge?joke=%s' % joke)
res_json = json.loads(res.text)
print('''
ダジャレ判定
    - ダジャレ：{}
    - レスポンス：{}
'''.format(joke, res_json))
