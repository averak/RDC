# -*- coding: utf-8 -*-

'''
ダジャレ判定の精度を計測
'''

import sys
import engine
import json
import glob
from tqdm import tqdm



jokes = []
for file in glob.glob('data/raw/*.json'):
    jokes.extend(json.load(open(file, 'r')))


# 判定モデルの計測
if 'judge' in sys.argv:
    result = 0  # 正解数
    for joke in tqdm(jokes):
        try:
            if joke['is_joke'] == engine.is_joke(joke['joke']):
                result += 1
        except:
            raise ValueError('判定に失敗：%s' % joke['joke'])


    print('精度：%f' % (result / len(jokes)))


# 評価モデルの計測
if 'evaluate' in sys.argv:
    model = engine.Evaluate(False)
    for joke in tqdm(jokes):
        score = model.predict(joke['joke'])
        star =  '★' * int(score)
        if score - int(score) > 0.5:
            star += '★'
        star += '☆' * (5-len(star))
        judge = engine.is_joke(joke['joke'])

        print('{}\n    - ダジャレ判定：{}'.format(joke['joke'], judge))
        if judge:
            print('    - ダジャレ評価：{} ({})'.format(star, score))

