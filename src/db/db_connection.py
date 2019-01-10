from pymongo import MongoClient
from config import Config

"""
DB接続クラス
"""
class DbConnection:
    _dbs = Config.get_db_section()

    """
    DB接続
    """
    def __init__(self):
        _client = MongoClient(self._dbs["IP_ADDRESS"], int(self._dbs["PORT"]))
        _client.admin.authenticate(self._dbs["ID"], self._dbs["PASS"])
        self._db = _client.AUTO_TRADE_DB