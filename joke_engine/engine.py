# -*- coding: utf-8 -*-
import re
from janome.tokenizer import Tokenizer


t = Tokenizer()


def to_katakana(sentence):
    ## -----*----- カタカナ変換 -----*----- ##
    katakana = ''
    for token in t.tokenize(sentence):
        s = token.reading
        if re.match('^[ァ-ンヴー]*$', s) != None:
            katakana += s

    return katakana


def is_joke(sentence):
    ## -----*----- ダジャレ判定 -----*----- ##
    # カタカナに変換
    katakana = to_katakana(sentence)
    # カタカナの長さ
    l_katakana = len(katakana)
    print(re.match('^[ァ-ンヴー]*$', katakana).group())
    print(l_katakana)

if __name__ == '__main__':
    print(to_katakana('遠距離恋愛'))
    is_joke('遠距離恋愛')
