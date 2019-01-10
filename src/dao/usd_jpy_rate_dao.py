import const #TODO 定数の作り修正
import sys
from db.db_connection import DbConnection

"""
実績値コレクションのDAO
"""
class UsdJpyRateDao(DbConnection):
    def __init__(self):
        super(UsdJpyRateDao, self).__init__()
        self._collection = sys.modules["const"].STUDY_COL