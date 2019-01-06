import oandapy
import time
import configparser
config = configparser.ConfigParser()
config.read("config.ini")
config.sections()

api_key = config["OANDA"]["api_key"]

oanda = oandapy.API(environment="practice", access_token= api_key)

def OandaTimeRate():
    time.sleep(1)
    response = oanda.get_prices(instruments="USD_JPY")
    prices = response.get("prices")
    asking_price = prices[0].get("ask")

    return asking_price

    # # DBの書き込み先を取得する
    # collection = getDBCollection("test_database")
    #
    # result = insertCollection("TIMERATE",prices[0])

    # コレクションにレコードを書き込みます
    # collection.insert(formatToInsert("instrument",prices[0].get("instrument")))
    # collection.insert(formatToInsert("time",prices[0].get("time")))
    # collection.insert(formatToInsert("bid",prices[0].get("bid")))
    # collection.insert(formatToInsert("ask",prices[0].get("ask")))

# if __name__ == "__main__":
#     Now = OandaTimeRate()
#     print(Now)