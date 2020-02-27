# -*- coding: utf-8 -*-

'''
ダジャレ判定の精度を計測
'''

import engine
import json
import glob
from tqdm import tqdm



jokes = []
for file in glob.glob('data/raw/*.json'):
    jokes.extend(json.load(open(file, 'r')))


# 計測
result = 0  # 正解数
for joke in tqdm(jokes):
    if joke['is_joke'] == engine.is_joke(joke['joke']):
        result += 1


print('精度：%f' % (result / len(jokes)))
