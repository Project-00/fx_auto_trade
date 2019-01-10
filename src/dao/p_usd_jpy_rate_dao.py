import pymongo
import const #TODO 定数の作り修正
import sys
from db.db_connection import DbConnection

"""
予測値コレクションのDAO
"""
class PUsdJpyRateDao(DbConnection):

    def __init__(self):
        super(PUsdJpyRateDao, self).__init__()
        self._collection = sys.modules["const"].PREDICTION_COL

    """
    売買判定用に最新の予測値ドキュメントを取得
    """
    def select_latest_one(self):
        return self._db[self._collection].find_one(
            {}
            , {
                "_id": 0
                , "open" : 1
                , "close": 1
                , "low" : 1
                , "high": 1
            }
            , sort=[("time", pymongo.DESCENDING)]
        )