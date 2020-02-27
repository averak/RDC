# -*- coding: utf-8 -*-
import re
from janome.tokenizer import Tokenizer


t = Tokenizer()


def to_katakana(sentence):
    ## -----*----- カタカナ変換 -----*----- ##
    katakana = ''

    # 形態素解析
    for token in t.tokenize(sentence):
        s = token.reading

        if s == '*':
            # 読みがわからないトークン
            if re.match('[ぁ-んァ-ンー]+', token.surface) != None:
                katakana += token.surface
        else:
            # 読みがわかるトークン
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

    # 1文字ずつずらしてn文字の要素を作成
    col = []
    for i in range(len(katakana)-n+1):
        col.append(katakana[i:(i+n)])

    if len(set(col)) != len(col):
        return True
    else:
        return False


if __name__ == '__main__':
    print(is_joke('遠距離恋愛'))
    print(is_joke('布団が吹っ飛んだ'))
    print(is_joke('つくねがくっつくね'))
    print(is_joke('ソースを読んで納得したプログラマ「そーすね」'))
    print(is_joke('布団が吹っ飛んだ'))
    print(is_joke('太古の太閤が太鼓で対抗'))
