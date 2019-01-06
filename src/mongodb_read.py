from pymongo import MongoClient
import pymongo
import os
import sys
import pandas as pd
from mongodb_write import getDBCollection
import pprint



def ReaDB(colName):

    # DBの読み込み先を取得する
    collection = getDBCollection(colName)

    db = collection
    cursor = db.find()
    df =pd.DataFrame.from_dict(list(cursor)).astype(object)

    return df

def mongodb_read(colName):

    df = ReaDB(colName)

    del df["_id"]

    df2 = df.ix[:,["time","close","open","high","low","volume","fiveave","tenave","fiftave"]]

    return df2

def mongod_read_find_one(colName,calm):

    collection = getDBCollection(colName)

    df2 = collection.find_one(calm)

    return df2