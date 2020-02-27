# -*- coding: utf-8 -*-

import os
import numpy as np
from tensorflow.keras import *
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import *
from tensorflow.keras.optimizers import *
from tensorflow.keras.models import *
from tensorflow.keras import Sequential


class Model(object):
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


    def __build(self, embed_size=32, max_length=30, filter_num=64, learning_rate=0.0005):
        ## -----*----- モデルをビルド -----*----- ##
        # モデルの定義
        model = Sequential([
            Input(shape=(max_length,)),
            Embedding(0xffff, embed_size,embeddings_regularizer=regularizers.l1(0.01)),
            Reshape((max_length, embed_size, 1)),
            Conv2D(filter_num, (2, embed_size), activation="relu", data_format='channels_first'),
            MaxPooling2D(pool_size=(max_length - 1, 1)),
            Conv2D(filter_num, (3, embed_size), activation="relu"),
            MaxPooling2D(pool_size=(max_length - 2, 1)),
            Conv2D(filter_num, (4, embed_size), activation="relu"),
            MaxPooling2D(pool_size=(max_length - 3, 1)),
            Conv2D(filter_num, (5, embed_size), activation="relu"),
            MaxPooling2D(pool_size=(max_length - 4, 1)),
            #Concatenate(),
            #Reshape((filter_num * len(filter_sizes),)),
            Flatten(),
            Dense(32, activation="relu"),
            #Dropout(0.5),
            BatchNormalization(),
            Dense(1, activation='sigmoid')
        ])

        # モデルをコンパイル
        model.compile(
            optimizer=Adam(lr=learning_rate),
            loss='binary_crossentropy',
            metrics=["accuracy"]
        )

        return model


    def __train(self, x, y):
        ## -----*----- 学習 -----*----- ##
        return


    def load_model(self):
        ## -----*----- モデル読み込み -----*----- ##
        # モデルが存在する場合に読み込む
        if os.path.exists(self.model_path):
            self.__model.load_weights(self.model_path)


if __name__ == '__main__':
    model = Model()

