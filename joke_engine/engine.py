# -*- coding: utf-8 -*-
import os, re
from janome.tokenizer import Tokenizer
import numpy as np
from tensorflow.keras import *
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import *
from tensorflow.keras.optimizers import *
from tensorflow.keras.models import *
from tensorflow.keras import Sequential
import json
import math
from kanjize import int2kanji
from tqdm import tqdm


class Evaluate(object):
    '''
    ダジャレを評価するモデル
    character-level CNNを用いて評価
    '''

    def __init__(self, train=True, model_path='model/model.hdf5'):
        # -----*----- コンストラクタ -----*----- ##
        # TensorFlowの警告レベルを設定
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        # モデルのビルド
        self.__model = self.__build()

        self.model_path = model_path

        if train:
            # 学習
            x, y = self.__features_extracter()
            self.__train(x, y)
        else:
            # モデルの読み込み
            self.load_model()


    def __build(self, embed_size=128, max_length=100, filter_sizes=(2, 3, 4, 5), filter_num=64, learning_rate=0.0005):
        ## -----*----- モデルをビルド -----*----- ##
        # Input Layer
        input_ts = Input(shape=(max_length, ))
        # Embedding 各文字をベクトル変換
        emb = Embedding(0xffff, embed_size)(input_ts)
        emb_ex = Reshape((max_length, embed_size, 1))(emb)
        # 各カーネルサイズで畳み込みをかける．

        convs = []
        # Conv2D
        for filter_size in filter_sizes:
            conv = Conv2D(filter_num, (filter_size, embed_size), activation='relu')(emb_ex)
            pool = MaxPooling2D((max_length - filter_size + 1 , 1))(conv)
            convs.append(pool)
        # ConcatenateでConv2Dを結合
        convs_merged = Concatenate()(convs)
        # Reshape
        reshape = Reshape((filter_num * len(filter_sizes),))(convs_merged)
        # Dense
        fc1 = Dense(64, activation='relu')(reshape)
        bn1 = BatchNormalization()(fc1)
        do1 = Dropout(0.5)(bn1)
        fc2 = Dense(1, activation='sigmoid')(do1)

        # Model generate
        model = Model(
            inputs=[input_ts],
            outputs=[fc2]
        )

        # モデルをコンパイル
        model.compile(
            optimizer=Adam(lr=learning_rate),
            loss='binary_crossentropy',
            metrics=["accuracy"]
        )

        return model


    def __train(self, x, y, batch_size=1000, epoch_count=1, max_length=30):
        ## -----*----- 学習 -----*----- ##
        self.__model.fit(
            x, y,
            nb_epoch=epoch_count,
            batch_size=batch_size,
            verbose=1,
            validation_split=0.2,
            shuffle=True,

        )

        # 最終の学習モデルを保存
        self.__model.save_weights(self.model_path)


    def __features_extracter(self, max_length=100):
        ## -----*----- 特徴量抽出 -----*----- ##
        x = [] # 入力
        y = [] # 正解ラベル

        # ダジャレ読み込み
        jokes = []
        jokes = json.load(open('data/raw/jokes.json', 'r'))

        # データセットを作成
        for joke in tqdm(jokes):
            katakana = to_katakana(joke['joke'])
            vec = [ord(x) for x in katakana]
            vec = vec[:max_length]
            if len(vec) < max_length:
                vec += ([0] * (max_length - len(vec)))

            if joke['score'] > 2.5:
                score = 1.0
            else:
                score = 0.0

            x.append(vec)
            y.append(score)

        x = np.array(x)
        y = np.array(y)

        return x, y


    def load_model(self):
        ## -----*----- モデル読み込み -----*----- ##
        # モデルが存在する場合に読み込む
        if os.path.exists(self.model_path):
            self.__model.load_weights(self.model_path)


    def predict(self, sentence, max_length=100):
        ## -----*----- 推論 -----*----- ##
        katakana = to_katakana(sentence)
        vec = [ord(x) for x in katakana]
        vec = vec[:max_length]
        if len(vec) < max_length:
            vec += ([0] * (max_length - len(vec)))

        score = self.__model.predict(np.array([vec]))
        score = 5.0 / (1.0 +  math.e**(-(25*score[0][0]-12.3)))

        n = 0
        for i in range(2, 6):
            if is_joke(sentence, i):
                n = i
        if   n<2:
            score += -1.5
        elif n==2:
            score += -1
        elif n==3:
            score += -0.3
        elif n==4:
            score += 0
        elif n==5:
            score += 0.3

        if score < 1: score = 1.0
        if score > 5: score = 5.0

        return score



t = Tokenizer()


def to_katakana(sentence, rm_ltu=False):
    ## -----*----- カタカナ変換 -----*----- ##
    '''
    sentence：判定対象の文
    rm_ltu：「っ」を削除するかどうか
    '''
    katakana = ''

    # 数字 -> 漢数字
    while re.match('\d+', sentence):
        c = re.match('\d+', sentence).group()
        sentence = sentence.replace(c, int2kanji(int(c)))

    # 形態素解析
    for token in t.tokenize(sentence):
        s = token.reading

        if s == '*':
            # 読みがわからないトークン
            if re.match('[ぁ-んァ-ンー]', token.surface) != None:
                katakana += token.surface
        else:
            # 読みがわかるトークン
            if re.match('[ァ-ン]', s) != None:
                katakana += s

    if rm_ltu:
        katakana = katakana.replace('ッ', '')

    pair = [
        'ぁぃぅぇぉっゃゅょゎァィゥェォッャュョヮヂ',
        'アイウエオツヤユヨワアイウエオツヤユヨワジ'
    ]
    for i in range(len(pair[0])):
        katakana = katakana.replace(pair[0][i], pair[1][i])

    return katakana


def is_joke(sentence, n=3, rm_ltu=False):
    ## -----*----- ダジャレ判定 -----*----- ##
    '''
    sentence：判定対象の文
    n：文字を分割する単位
    rm_ltu：「っ」を削除するかどうか
    '''
    katakana = to_katakana(sentence, rm_ltu)

    # 1文字ずつずらしてn文字の要素を作成
    col = []
    for i in range(len(katakana)-n+1):
        col.append(katakana[i:(i+n)])

    if len(set(col)) != len(col):
        return True
    else:
        if 'ー' in katakana:
            return is_joke(katakana.replace('ー', ''))
        if not rm_ltu:
            if 'っ' in sentence or 'ッ' in sentence:
                if is_joke(sentence, rm_ltu=True):
                    return True
                else:
                    return is_joke(sentence.replace('っ', '').replace('ッ', ''))

        return False


if __name__ == '__main__':
    jokes = []
    jokes.append('遠距離恋愛')
    jokes.append('この皿はサラサラしてる')
    jokes.append('筋トレで金獲れ')
    jokes.append('布団が吹っ飛んだ')
    jokes.append('つくねがくっつくね')
    jokes.append('布団が吹っ飛んだ')
    jokes.append('ソースを読んで納得したプログラマ「そーすね」')
    jokes.append('太古の太閤が太鼓で対抗')

    model = Evaluate(False)

    for joke in jokes:
        score = model.predict(joke)
        star =  '★' * int(np.round(score))
        star += '☆' * (5-len(star))
        judge = is_joke(joke)

        print('{}\n    - ダジャレ判定：{}'.format(joke, judge))
        if judge:
            print('    - ダジャレ評価：{} ({})'.format(star, score))
        else:
            print('    - カタカナ変換：%s' % to_katakana(joke))

