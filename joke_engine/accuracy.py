# -*- coding: utf-8 -*-

'''
ダジャレ判定の精度を計測
'''

import sys
import engine
import json
import glob
import numpy as np
from tqdm import tqdm



jokes = []
for file in glob.glob('data/raw/*.json'):
    jokes.extend(json.load(open(file, 'r')))
jokes = json.load(open('data/raw/jokes.json', 'r'))[:500]

# 判定モデルの計測
if 'judge' in sys.argv:
    result = 0  # 正解数
    for joke in tqdm(jokes):
        try:
            if joke['is_joke'] == engine.is_joke(joke['joke']):
                result += 1
            #else:
            #    print('判定に失敗：%s' % joke['joke'])
        except:
            raise ValueError('エラー発生：%s' % joke['joke'])


    print('精度：%f' % (result / len(jokes)))

# 評価モデルの計測
if 'evaluate' in sys.argv:
    model = engine.Evaluate(False)
    scores = []
    map_score = [0, 0, 0, 0, 0]
    for joke in tqdm(jokes):
        if joke['is_joke']:
            score = model.predict(joke['joke'])
            scores.append(score)
            map_score[int(np.round(score))-1] += 1
            #'''
            star =  '★' * int(np.round(score))
            star += '☆' * (5-len(star))
            judge = engine.is_joke(joke['joke'])

            print('{}\n    - ダジャレ判定：{}'.format(joke['joke'], judge))
            if judge:
                print('    - ダジャレ評価：{} ({})'.format(star, score))
            #'''

    print('最大値：{}，最小値：{}'.format(max(scores), min(scores)))
    print(list(100*np.array(map_score)/len(jokes)))

