from pymongo import MongoClient
import sys
import configparser
config = configparser.ConfigParser()
config.read("config.ini")
config.sections()

IP_ADDRESS = config["DB"]["IP_ADDRESS"]
PORT = int(config["DB"]["PORT"])
ID = config["DB"]["ID"]
PASS = config["DB"]["PASS"]


#DBの書き込み先を取得する
def getDBCollection(collectionName):
    c=sys.modules["const"]

    # LocalhostのMongoDBに書き込みます


    client = MongoClient(IP_ADDRESS,PORT)
    client.admin.authenticate(ID, PASS)
    db = client.AUTO_TRADE_DB

    #コレクションの作成
    #db.createCollection(collectionName)

    # collectionというコレクションを使います
    collection = db[collectionName]

    return collection

# データを書き込み用に変形する
def formatToInsert(key, Contents):
    # DBの  "キー名"     : "データ"
    return {key: Contents}

def insertCollection(collectionName,post):
    collection = getDBCollection(collectionName)

    # idは自動で一意に振り分けられる
    result = collection.insert_one(post)
    return result

