import configparser

class Config:
    """
    config.iniの読み込み
    """
    @staticmethod
    def _read_sections():
        config = configparser.ConfigParser()
        config.read("/src/config.ini") #TODO pathの書き方全体で統一
        config.sections()
        return config

    """
    DBセクションの取得
    """
    @staticmethod
    def get_db_section():
        return Config._read_sections()["DB"]

    """
    OANDAセクションの取得
    """
    @staticmethod
    def get_oanda_section():
        return Config._read_sections()["OANDA"]