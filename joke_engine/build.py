# -*- coding: utf-8 -*-
import os, sys, re
import json
import time
import glob
import pycrawl
from tqdm import tqdm



def fetch_jokes(delay=3.0, depth_limit=None):
    ## -----*----- ダジャレ一覧を取得 -----*----- ##
    '''
    delay：アクセス間隔 [s]
    depth_limit：クロールする深さ（None->無限）
    '''

    url = 'https://dajare.jp/search/'
    agent = pycrawl.PyCrawl(url)

    # ダジャレ一覧（ヘッダーを削除）
    jokes = agent.css('.List').css('tr')[1:]
    ret = []

    # クロールする深さを決定
    if depth_limit == None:
        n_jokes = agent.xpath('//*[@id="PanelContentMain"]/p[2]/span').inner_text()
        depth_limit = \
            int(re.match('\d+', n_jokes).group()) // 100

    for i in tqdm(range(depth_limit)):
        try:
            for el in jokes:
                ret.append({})

                ret[-1]['joke'] = el.css('a').inner_text()
                ret[-1]['score'] = float(re.match(r'\d.\d', el.css('.ListWorkScore').inner_text()).group())
                ret[-1]['is_joke'] = True

            # Next Page
            agent.submit(id='FormButtonNext')
            time.sleep(delay)

        except:
            break

    return ret


if __name__ == '__main__':
    # ダジャレ一覧を取得
    if 'fetch' in sys.argv:
        jokes = fetch_jokes(0.5)
        json.dump(jokes, open('data/raw/jokes.json','w'), indent=4)

    if 'json' in sys.argv:
        files = glob.glob('data/raw/*.json')
        print(files)
        #json.load(open('data/raw/*.json', 'r'))

