import datetime
from datetime import datetime as dt
from datetime import timedelta
from datetime import timezone
from pymongo import MongoClient
from mongodb_write import getDBCollection
from mongodb_write import insertCollection




# 時間を取る関数
def GetHour():

    #時の取得
    gethour = dt.now().hour
    #確認出力
    #print(gethour)

    return gethour

# 日にちを取る関数
def GetDate():

    DLT = timezone(timedelta(hours=+0), 'DLT')

    #日にちの取得
    getnow = dt.now(DLT)

    gettime = getnow.strftime('%Y/%m/%d')
    #確認出力
    #print(gettime)

    return gettime


def GetDocSingleData(clmData,docKey,ad):

    #時刻呼び出し
    nowhour = GetHour()
    nowDate = GetDate()

    # データベースの呼び出し
    client = MongoClient("localhost", 27017)

    mongo_client = MongoClient('localhost:27017')
    db_connect = mongo_client["test_database"]

    # データを取得する
    #始値
    docData = db_connect["TIMERATE"].find({"time":{"$regex": nowDate}}).sort(docKey ,ad).limit(1)

    for data in docData:
        result = data[clmData]

    return result

#曜日データを格納する関数
def GetDayoftheweek():
    DLT = timezone(timedelta(hours=+0), 'DLT')
    #曜日データ取得
    Dotw = dt.now(DLT)
    getDotw = Dotw.weekday()

    return getDotw

# 日付をずらす関数
def LateDate(nowDay):

    # 現在の日付を入力した際、0日になるのを回避するため（1日の時等に0日になってしまう）
    NowDay = nowDay - 1
    DLT = timezone(timedelta(hours=+0), 'DLT')

    #日にちの取得
    getnow = dt.now(DLT) - timedelta(days=NowDay)


    gettime = getnow
    #確認出力
    #print(gettime)

    return gettime



def insertStudyData():

    #日付
    nowDate = GetDate()
    #曜日
    nowWeekday = GetDayoftheweek()
    #始値
    startValue = GetDocSingleData("ask","time",-1)
    # 高値
    highValue = GetDocSingleData("ask","ask",-1)
    # 安値
    lowValue = GetDocSingleData("ask","ask",1)
    # 終値
    endValue = GetDocSingleData("ask", "time", 1)

    #それぞれの値を格納
    point = {
        "DATE": nowDate,
        "WEEKDAY":nowWeekday,
        "STARTVALUE": startValue,
        "HIGHVALUE":highValue,
        "LOWVALUE":lowValue,
        "ENDVALUE":endValue
    }

    #studypointというDBにpointのデータを格納する
    result = insertCollection("STUDYPOINT", point)
    return True