import json


class CodeInfo:
    def __init__(self):
        self.id = 0
        self.code = ""
        self.symbol = ""
        self.name = ""
        #  地区
        self.area = ""
        # 行业
        self.industry = ""
        # 市场
        self.market = ""
        # 上市时间
        self.list_date = ""

    def __str__(self):
        return self.__dict__.__str__()


class DailyInfo:
    def __init__(self):
        self.id = 0
        self.code = 0
        # 日期
        self.trade_date = 0
        # 开盘价
        self.open = 0
        # 最高价
        self.high = 0
        # 最低价
        self.low = 0
        # 收盘价
        self.close = 0
        # 昨日收盘价
        self.pre_close = 0
        # 涨跌点（今收-昨收）
        self.change = 0
        # 涨跌幅（%）
        self.pct_chg = 0
        # 成交量（手）
        self.vol = 0
        # 成交额（千元）
        self.amount = 0

    def __str__(self):
        return self.__dict__.__str__()


class Hs300ElementInfo:
    def __init__(self):
        self.SECUCODE = ""
        self.SECURITY_CODE = ""
        self.TYPE = ""
        self.SECURITY_NAME_ABBR = ""
        self.CLOSE_PRICE = ""
        self.INDUSTRY = ""
        self.REGION = ""
        self.WEIGHT = ""
        self.EPS = ""
        self.BPS = ""
        self.ROE = ""
        self.TOTAL_SHARES = ""
        self.FREE_SHARES = ""
        self.FREE_CAP = ""
        self.f2 = ""
        self.f3 = ""

    def __str__(self):
        return self.__dict__.__str__()


class QuotaInfo(DailyInfo):
    def __init__(self):
        super(QuotaInfo, self).__init__()
        #   macd指标相关
        self.DIF = "DIF"
        self.DEA = "DEA"
        self.MACDHIST = "MACDHIST"
        #   DIF斜率
        self.DIF_S = "DIF_S"
        self.DEA_S = "DEA_S"
        self.MACDHIST_S = "MACDHIST_S"
        #   DIF与DEA的交点
        self.MACD_CROSS = "MACD_CROSS"

        #   RSI指标相关
        self.RSI6 = "RSI6"
        self.RSI6_TYPE = "RSI6_TYPE"
        self.RSI12 = "RSI12"
        self.RSI12_TYPE = "RSI12_TYPE"
        self.RSI24 = "RSI24"
        self.RSI24_TYPE = "RSI24_TYPE"

        #   ma指标相关
        self.MA5 = "MA5"
        self.MA10 = "MA10"
        self.MA20 = "MA20"
        self.MA60 = "MA60"
        self.MA120 = "MA120"
        self.MA250 = "MA250"
        #   ma5 与ma60的交点
        self.MA5_60_CROSS = "MA5_60_CROSS"
        #   ma的斜率
        self.MA5_SLOPE = "MA5_SLOPE"
        self.MA10_SLOPE = "MA10_SLOPE"

        #   成交量的ma
        self.VOLUME_MA120 = "VOLUME_MA120"
        #   当日成交量与ma120的交点
        self.VOLUME_120_CROSS = "VOLUME_120_CROSS"
        #   当日成交量与ma120的差值
        self.VOLUME_DIFF = "VOLUME_DIFF"

        #   ema
        self.EMA30 = "EMA30"
        self.EMA200 = "EMA200"

        #   dmi
        self.PDI = "PDI"
        self.MDI = "MDI"
        self.ADX = "ADX"
        self.ADXR = "ADXR"
        #   ADX是否大于50
        self.ADX_TYPE = "ADX_TYPE"
        #   斜率
        self.PDI_S = "PDI_S"
        self.MDI_S = "MDI_S"
        #   差值
        self.PM_DIFF = "PM_DIFF"

def parse(json_str, obj):
    d = json.loads(json_str)
    result = obj()
    result.__dict__ = d
    return result


def toJson(obj):
    return json.dumps(obj.__dict__)


if __name__ == '__main__':
    # ci=CodeInfo()
    #
    # ci.id=1
    # print(toJson(ci))
    p = parse('{"id": 1,  "symbol": "", "area": "", "industry": "", "market": "", "list_date": ""}', CodeInfo)
    print(p)
