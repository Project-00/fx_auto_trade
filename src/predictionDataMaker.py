# -*- coding: utf-8 -*-
# ライブラリのインポート
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error
from mongodb_read import mongodb_read
import sys

# -- 学習データ加工部分 --

def predictionDataMaker(parameter):
    # OANDAAPI のドル円１日足を取得して扱いやすくしたデータを用いているため注意。（要工夫）
    # CSVファイルの読み込み（）内で指定
    # 内容の順は time（時間） close（終） open（始） high（高） low（低） volume（取引数）　の順
    # 要素を増やすことでより精度が上がる模様
    # df = pd.read_csv("./__csv__/" + csvfile)

    # 定数呼び出し
    c=sys.modules["const"]

    df = mongodb_read(c.STUDY_COL)
    df = df.sort_values(by="time")
    df = df.reset_index()


    # parameter毎に順序切り替え
    if parameter == c.CLOSE:
        df = df.ix[:, ["time", "close", "open", "high", "low", "volume","fiveave","tenave","fiftave"]]
        prm = ["close"]
    if parameter == c.OPEN:
        df = df.ix[:, ["time", "open", "close", "high", "low", "volume","fiveave","tenave","fiftave"]]
        prm = ["open"]
    if parameter == c.HIGH:
        df = df.ix[:, ["time", "high", "close", "open", "low", "volume","fiveave","tenave","fiftave"]]
        prm = ["high"]
    if parameter == c.LOW:
        df = df.ix[:, ["time", "low", "close", "open", "high", "volume","fiveave","tenave","fiftave"]]
        prm = ["low"]
    if parameter == c.FIVEAVE:
        df = df.ix[:, ["time", "fiveave", "close", "open", "high", "volume","low","tenave","fiftave"]]
        prm = ["fiveave"]
    if parameter == c.TENAVE:
        df = df.ix[:, ["time", "tenave", "close", "open", "high", "volume","low","fiveave","fiftave"]]
        prm = ["tenave"]
    if parameter == c.FIFTAVE:
        df = df.ix[:, ["time", "fiftave", "close", "open", "high", "volume","low","fiveave","tenave"]]
        prm = ["fiftave"]

    print(parameter + "を計算します")
        
    df_test = df.tail(1)

    # 一番左の列を１日分移動上に(prmの位置はデータによるので要注意)
    df_shift = df.copy()
    df_shift[prm] = df_shift[prm].shift(-1)

    # 念のためデータをdf_2として新しいデータフレームへコピー
    # 加工元のデータを変えないようにするための措置
    df_2 = df_shift.copy()

    # 最後尾はいらないので除去
    lastnum = len(df_2) - 1 # データ行数を求める（個数　-　1）で最後行を見つける
    df_2 = df_2.drop(lastnum)  # データの最後尾を削除する
    # time(時間)を消去
    del df_2["time"]
    del df_test["time"]



    # データセットの行数と列を格納
    n = df_2.shape[0]  # 行
    p = df_2.shape[1]  # 列

    # 訓練データとテストデータへ切り分け
    train_start = 0
    train_end = int(np.floor(n))  # 前から数えて行全体の８割を教師データとして扱う
    # test_start = train_end   # 教師データ以降のデータをテストデータとして扱う
    # test_end = n
    data_train = df_2[train_start:train_end]  # トレーニングの幅の設定
    # data_test = df_2[test_start:test_end]  # テストの幅の設定
    # data_train = df_2
    data_test = df_test  # テストの幅の設定

    # データの正規化
    scaler = MinMaxScaler(feature_range=(-1, 1))  # -1から1の範囲に正規化する設定
    scaler.fit(data_train)  # 教師データを元に正規化設定（テストデータは必要ない）

    # norm→ノーマライゼーション（正規化の略称）
    data_train_norm = scaler.transform(data_train)  # 教師データの正規化
    data_test_norm = scaler.transform(data_test)  # テストデータの正規化

    # 特徴量とターゲットへ切り分け
    X_train = data_train_norm[:, 1:]  # 説明関数（出力を求める素材）    列   0   1    2    3   4
    X_test = data_test_norm[:, 1:]  # closeを除く他の要素を選択している(close,open,high,low,volume)
    Y_train = data_train_norm[:, 0]  # 目的関数（出力を予想する）
    Y_test = data_test_norm[:, 0]  # closeだけを選択している

    # 訓練データの説明関数を取得
    n_stocks = X_train.shape[1]  # 説明関数の列数（close 等の要素の種類の数）

    return X_train, X_test, Y_train, Y_test, scaler, n_stocks

# 値の呼び出し方のメモ
# if __name__ == "__main__":
#     tdm = trainDataMaker("usd_jpy_api.csv")
#
#     X_train = tdm[0]
#     X_test = tdm[1]
#     Y_train = tdm[2]
#     Y_test = tdm[3]
#     scaler = tdm[4]
#     n_stocks = tdm[5]
#
#     print(X_train)
#     print(X_test)
#     print(Y_train)
#     print(Y_test)
#     print(scaler)
#     print(n_stocks)

# if __name__ == "__main__":
#     p = predictionDataMaker("OPEN")ss