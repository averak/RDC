# -*- coding: utf-8 -*-
import os, sys, re
import json
import pycrawl


url = 'https://dajare.jp/search/'
agent = pycrawl.PyCrawl(url)


def fetch_jokes(delay=3.0, depth_limit=None):
    ## -----*----- ダジャレ一覧を取得 -----*----- ##
    '''
    delay：アクセス間隔 [s]
    depth_limit：クロールする深さ（None->無限）
    '''
    # ダジャレ一覧（ヘッダーを削除）
    jokes = agent.css('.List').css('tr')[1:]

    ret = []

    for el in jokes:
        ret.append({})

        ret[-1]['joke'] = el.css('a').inner_text()
        ret[-1]['score'] = float(re.match('\d.\d', el.css('.ListWorkScore').inner_text()).group())
        print(ret[-1])


if __name__ == '__main__':
    fetch_jokes()
