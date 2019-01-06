# -*- coding:utf8 -*-
import mongodb_write
from mongodb_read import mongodb_read
from datetime import datetime,timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import *
from mongodb_write import insertCollection
import const
import sys

# この関数を使うときは、USD_JPY_RATEの状態を最新状態にする必要がある。
# 順序的に言えば、USD_JPY_RATEの更新→平均の算出でなければ正確な値は出ない

c = sys.modules["const"]

# 汎化型day日平均を求める関数
# 整頓されたデータフレーム型を対象とする
# key: 要素番号（ループ処理で利用）
# day: 何日平均で取りたいかを入力
# df: ソートして整頓されたデータフレームを引数に入れること
def dfAverage(key,day,df):

    # 要素番号（日付順）をday分遡って範囲を指定する
    Ave = df[key - day : key]
    # closeの部分を取り出す
    Ave = Ave.close
    # 平均を求める
    result = Ave.mean()

    return result

def ListAverage(key,day,list):

    # 要素番号（日付順）をday分遡って範囲を指定(close)
    Ave = list[key - day : key]
    # 平均を求める
    result = np.mean(Ave)

    return result


def MakeMovingAverage():

    # モンゴDBからtimeとcloseを取ってくる
    df = mongodb_read()
    df = df.sort_values(by="time")
    df = df.reset_index()
    df = df[["time","close"]]

    # 格納リスト作成
    fivelist = []
    tenlist = []
    fiftlist = []
    # twenlist = []

    # time毎に5日平均を回す！（前から５番目まで飛ぶ）
    for i in range(5,len(df)):

        Five = dfAverage(i,5,df)

        # Five出力結果のリストの作成
        fivelist.append(Five)

    # 25日移動平均の要素数に合わせてデータを削除(20行分)
    del fivelist[:20]


    # time毎に10日平均を回す！（前から１０番目まで飛ぶ）
    for j in range(10,len(df)):

        Ten = dfAverage(j,10,df)

        # Ten出力結果のリストの作成
        tenlist.append(Ten)

    # 25日移動平均の要素数に合わせてデータを削除(15行分)
    del tenlist[:15]

    for k in range(15,len(df)):

        Fift = dfAverage(k,15,df)

        fiftlist.append(Fift)


    # # time毎に25日平均を回す(前から２５番目まで飛ぶ)
    # for k in range(25,len(df)):
    #
    #     Twen = dfAverage(k,25,df)
    #
    #     # Twen出力結果リストの作成
    #     twenlist.append(Twen)

    # 15日分のデータフレームを除去、timeだけ残す
    df = df.time
    dflist = df.tolist()
    del dflist[:15]

    # ２５日平均に数を合わせたので、辞書登録まわし
    for x in range(len(fiftlist)):

        d = {"time":dflist[x] ,"fiveave":fivelist[x],"tenave":tenlist[x],"fiftave":fiftlist[x]}

        result = insertCollection(c.MOVINGAVERAGE_COL, d)

# if __name__ == "__main__":
#
#     collection = mongodb_write.getDBCollection(c.MOVINGAVERAGE_COL)
#     collection.remove()
#     result = MakeMovingAverage()
