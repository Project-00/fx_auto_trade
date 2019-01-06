# -*- coding: utf-8 -*-

import oandapy
import pandas as pd
import configparser
config = configparser.ConfigParser()
config.read("config.ini")
config.sections()

# チュートリアル講座のアカウント情報

account_id = int(config["OANDA"]["account_id"])
api_key = config["OANDA"]["api_key"]

oanda = oandapy.API(environment="practice", access_token=api_key)

# ----------トレードの管理系関数群--------------

# 口座の詳細情報を取得する関数
def ResponsAccountDetail():
    res_acct_detail = oanda.get_account(account_id= account_id)
    # balance: 口座残高
    # realizedPI: 実現損益
    # unrealizedPI: 評価損益
    return res_acct_detail

# オープントレードを取得(未決済のトレード表示)
def OpenOrder():
    open_orders = oanda.get_orders(account_id= account_id)

    return open_orders

# トレード情報を取得
def Trades():
    trades = oanda.get_trades(account_id= account_id)
    trades = pd.DataFrame(trades["trades"])

    return trades

# トレード履歴を取得
# count :　取得件数を入力
def HistricalTrade(count):
    trade_hist = oanda.get_transaction_history(account_id= account_id,count= count)
    trade_hist = pd.DataFrame(trade_hist["transactions"])

    return trade_hist



# -------------注文する関数群----------------

# ストリーミング成行注文
# unitsは通貨量（ドル指定なら1000ドル,円指定なら1000円）統一化する量:　数字
# sideは買い側か売り側か等を入力(売り:"sell",買い:"buy")
def Order(Price,Units,Side):
    order = oanda.create_order(account_id= account_id,
                               instrument = "USD_JPY",
                               price = Price,
                               units = Units,
                               side = Side,
                               type = "market")

    return order

# 指値注文
# LimitTimeには有効期限を入力すること
# Priceには値段を入れる
# Unitsには通貨量をいれる
# Sideには買い側か売り側か入力(売り:"sell",買い:"buy")
def LimitOrder(LimitTime,Price,Units,Side):
    limit_order = oanda.create_order(account_id= account_id,
                                     instrument = "USD_JPY",
                                     price = Price,
                                     units = Units,
                                     side = Side,
                                     expiry = LimitTime,
                                     type = "limit"
                                     )
    return limit_order

# 逆指値注文
# LimitTimeには有効期限を入力すること
# Priceには値段を入れる
# Unitsには通貨量をいれる
# Sideには買い側か売り側か入力(売り:"sell",買い:"buy")
def StopOrder(LimitTime,Price,Units,Side):
    stop_order = oanda.create_order(account_id= account_id,
                                    instrument = "USD_JPY",
                                    price = Price,
                                    units = Units,
                                    side = Side,
                                    expiry = LimitTime,
                                    type = "stop"
                                    )
    return stop_order

# 成行注文(OCO注文)（利益確定と損切りの指定）
# High: 利益確定レート
# Low: 損切りレート
# Unitsには通貨量をいれる
# Sideには買い側か売り側か入力(売り:"sell",買い:"buy")
def MKOrder(High,Low,Units,Side):
    order_mk = oanda.create_order(account_id= account_id,
                                  instrument="USD_JPY",
                                  units= Units,
                                  side= Side,
                                  takeProfit= High,
                                  stopLoss= Low,
                                  type="market")
    return order_mk

# 注文を変更する関数
# オープントレードからオーダーIDを取得してOrder_idにいれること
# Priceには希望価格を入力
# unitsには通貨量を入力
def ChangeOrder(Order_id,Price,Units):
    changeorder = oanda.modify_order(account_id= account_id,
                                     instrument = "USD_JPY",
                                     order_id=Order_id,
                                     price=Price,
                                     units=Units)

    return changeorder

# if __name__ == "__main__":
#
#     test = OpenOrder()
#     print(test)