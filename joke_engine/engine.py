# -*- coding: utf-8 -*-
import re
from janome.tokenizer import Tokenizer


t = Tokenizer()


def to_katakana(sentence):
    ## -----*----- カタカナ変換 -----*----- ##
    katakana = ''
    for token in t.tokenize(sentence):
        s = token.reading
        if s == '*' and re.match('[\u3041-\u309Fー]+', token.base_form) != None:
            s = token.base_form
        if re.match('^[ぁ-んァ-ンヴー]*$', s) != None:
            katakana += s

    katakana = katakana.replace('ッ', '')
    pair = [
        'ぁぃぅぇぉっゃゅょゎァィゥェォッャュョヮ',
        'アイウエオツヤユヨワアイウエオツヤユヨワ'
    ]
    for i in range(len(pair[0])):
        katakana = katakana.replace(pair[0][i], pair[1][i])

    return katakana


def is_joke(sentence, n=3):
    ## -----*----- ダジャレ判定 -----*----- ##
    # カタカナに変換
    katakana = to_katakana(sentence)
    print(katakana)
    # カタカナの長さ
    l_katakana = len(katakana)

    # 1文字ずつずらしてn文字の要素を作成
    col = []
    for i in range(l_katakana-n+1):
        col.append(katakana[i:(i+n)])

    if len(set(col)) != len(col):
        return True
    else:
        return False


if __name__ == '__main__':
    print(is_joke('遠距離恋愛'))
    print(is_joke('つくねがくっつくね'))
    print(is_joke('ソースを読んで納得したプログラマ「そーすね」'))
    print(is_joke('布団が吹っ飛んだ'))
