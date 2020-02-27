# -*- coding: utf-8 -*-

import os
import numpy as np
from tensorflow.keras import *
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import *
from tensorflow.keras.optimizers import *
from tensorflow.keras.models import *
from tensorflow.keras import Sequential


class Evaluate(object):
    '''
    ダジャレを評価するモデル
    character-level CNNを用いて評価
    '''

    def __init__(self, train=True, model_path='model/model.hdf5'):
        # -----*----- コンストラクタ -----*----- ##
        # モデルのビルド
        self.__model = self.__build()
        return

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


    def load_model(self):
        ## -----*----- モデル読み込み -----*----- ##
        # モデルが存在する場合に読み込む
        if os.path.exists(self.model_path):
            self.__model.load_weights(self.model_path)


if __name__ == '__main__':
    model = Evaluate()

