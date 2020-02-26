# -*- coding: utf-8 -*-
from janome.tokenizer import Tokenizer

t = Tokenizer()

def to_katakana(sentence):
    ## -----*----- カタカナ変換 -----*----- ##
    katakana = [token.reading for token in t.tokenize(sentence)]

    return ''.join(katakana)

if __name__ == '__main__':
    print(to_katakana('遠距離恋愛'))
