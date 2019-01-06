# -*- coding:utf-8 -*-
import mongodb_write
import sys
import previousDataOanda

# 定数呼び出し
c=sys.modules["const"]

# コレクション取得
collection = mongodb_write.getDBCollection(c.STUDY_COL)

# データ削除
collection.remove()
print("既存データの削除をしました")

# データ登録
result = previousDataOanda.historyData(c.YEAR, 20, 1)

print("完了")