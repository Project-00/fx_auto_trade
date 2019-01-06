import oandapy
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from makeStudyData import LateDate
from mongodb_write import insertCollection
import workdays
from MovingAverage import ListAverage
import const
import sys

oanda = oandapy.API(environment="practice", access_token="806baeb6718f153657980002fea49c6c-2cf6534cb404c014c63931f73fa3def7")
# 定数定義呼び出し
c = sys.modules["const"]

# five = 5日移動平均
# ten = 10日移動平均
# fift = 15日移動平均
# 一日分だけ登録する
def oneListWriteForMongo(list1,five,ten,fift):
    d = {"time": list1[0].get('time')[:10].replace('-', '/'), "close": list1[0].get('closeBid'),
         'open': list1[0].get('openBid'),
         'high': list1[0].get('highBid'), 'low': list1[0].get('lowBid'),
         'volume': list1[0].get('volume'), 'fiveave': five[0], 'tenave': ten[0], 'fiftave': fift[0]}

    # USD_JPY_RATEに格納
    result = insertCollection(c.STUDY_COL, d)

    return result



# oandaから出てきたリストと移動平均のリストを一括で加工する関数
def ListWriteForMongo(list1,list2,list3,list4):
    # 移動平均用のループカウンタ
    k = 0
    # 15番目からスタートして最後まで（15日平均に合わせる）
    for j in range(15,len(list1)):

        d = {"time": list1[j].get('time')[:10].replace('-','/'), "close": list1[j].get('closeBid'), 'open': list1[j].get('openBid'),
             'high': list1[j].get('highBid'), 'low': list1[j].get('lowBid'),
             'volume': list1[j].get('volume'),'fiveave':list2[k],'tenave':list3[k],'fiftave':list4[k]}
        # 移動平均用のループ更新
        k+=1
        # USD_JPY_RATEに格納
        result = insertCollection(c.STUDY_COL, d)

    return result


# parame:年月日（Y M D）が入ってくる
# count:ループ回数
# nowDay:月毎や年毎で1日始めで取りたいときに使う。特に指定しない場合は 1 を入力しておく。当日の日付を入力することで1日初めに矯正する。
def historyData(prm,count,nowDay):

    # nowDayに入った数だけ日付を減算することで、１日目からの取得に変えれる。変えない場合はnowDayに１を入れておく。
    Time = LateDate(nowDay)

    # 初期定義
    endtime = Time
    # count の回数だけ１年ずつ遡って処理する
    if (prm == c.YEAR):
        # 初期定義
        # 日取りしたい場合は何日分のデータが欲しいかカウントに代入
        # 更新定義(その年によってワークカウントが変わる可能性を考慮)
        # 一年間の範囲を取得
        one_year_ago = endtime - relativedelta(months=12)
        workcount = workdays.networkdays(one_year_ago, endtime)
        endtime = Time.isoformat('T')

        # 登録データ
        usdJpyDataList = []
        fiveList = []
        tenList = []
        fiftList = []

        # countの数だけ年数を遡ってデータを取得する
        for i in range(count):

            response = oanda.get_history(instrument = "USD_JPY", granularity = "D",end= endtime, count= workcount)
            USD_JPY_D1 = response.get("candles")

            # # list(USD_JPY_D1)をdict型にデータを抜き出し加工する
            # d = ListWriteForMongo(USD_JPY_D1)
            for j in USD_JPY_D1:
                usdJpyDataList.append(j)

            # weekday = dt.strptime(endtime.replace('/', '-') + " 06:00:00", '%Y-%m-%d %H:%M:%S').weekday()

            # 先頭のデータのtimeを取得して、RFC3339フォーマットをpythonのdatetimeフォーマットに変換
            dtime = dt.strptime(USD_JPY_D1[0]['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            # 取得したdtimeから１年（１２か月）引いて１年前を求める
            one_year_ago = dtime - relativedelta(months=12)
            # dtimeからdtimeの１年前までの期間の営業日を求める
            workcount = workdays.networkdays(one_year_ago, dtime)
            # もう一度RFC3339フォーマットに変換
            endtime = dtime.isoformat('T')

        # リストを日付順にソートする
        usdJpyDataList.sort(key=lambda x: x['time'])

        # 5日平均、10日平均、25日平均のリストを作成
        # 25日平均に合わせて要素を削除
        Closelist = []
        for w in range(len(usdJpyDataList)):
            Closelist.append(usdJpyDataList[w].get("closeBid"))

        for x in range(5,len(Closelist)):
            five = ListAverage(x,5,Closelist)
            fiveList.append(five)
        del fiveList[:10]

        for y in range(10,len(Closelist)):
            ten = ListAverage(y,10,Closelist)
            tenList.append(ten)
        del tenList[:5]

        for z in range(15,len(Closelist)):
            fift = ListAverage(z,15,Closelist)
            fiftList.append(fift)

        # list1(USD_JPY_D1)をdict型にデータを抜き出し加工する
        # list2(fiveAve)
        # list3(tenAve)
        # list4(twenAve)
        d = ListWriteForMongo(usdJpyDataList,fiveList,tenList,fiftList)


    # 年同様の動きをする
    elif (prm == c.MONTH):

        one_month_ago = endtime - relativedelta(months=1)
        workcount = workdays.networkdays(endtime, one_month_ago)

        for i in range(count):

            response = oanda.get_history(instrument = "USD_JPY", granularity = "D",end= endtime, count= workcount)
            USD_JPY_D1 = response.get("candles")

            # list(USD_JPY_D1)をdict型にデータを抜き出し加工する
            d = ListWriteForMongo(USD_JPY_D1)

            # USD_JPY_RATEに格納
            result = insertCollection(c.STUDY_COL, d)

            # 先頭のデータのtimeを取得して、RFC3339フォーマットをpythonのdatetimeフォーマットに変換
            dtime = dt.strptime(USD_JPY_D1[0]['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            one_month_ago = dtime - relativedelta(months=1)
            workcount = workdays.networkdays(one_month_ago, dtime)
            # もう一度RFC3339フォーマットに変換
            endtime = dtime.isoformat('T')


    # １日だけ動く(1日分のデータ取得)
    elif (prm == c.DAY):

        response = oanda.get_history(instrument="USD_JPY", granularity="D", end=endtime, count=1)
        USD_JPY_D1 = response.get("candles")

        # list(USD_JPY_D1)をdict型にデータを抜き出し加工する
        d = ListWriteForMongo(USD_JPY_D1)

        # USD_JPY_RATEに格納
        result = insertCollection(c.STUDY_COL, d)


#
# if __name__ == "__main__":
#
#     # 引数は　年月日コード　取りたい年数分　当日以前ならば１、月の頭（１日）からなら現在日付けを入力
#     result = historyData(c.YEAR,20,1)
#
#     print("終わりました")