


class FileConfig():
    #   交易日历路径
    CALENDAR_PATH=r"E:\data\webstock\calender.csv"
    #   股票列表
    CODEDETAIL_PATH = r"E:\data\webstock\code_detail.csv"
    #   沪深300成分股
    CODEHS300ELEMENT_PATH = r"E:\data\webstock\quota\hs300"
    #   沪深300历史数据
    CODEHS300HISTORY_PATH = r"E:\data\webstock\quota\hs300\hs300.csv"
    #   股票历史数据
    CODEHISTORY_PATH = r"E:\data\webstock\stock_daily"
    #   股票指标
    CODEQUOTA_PATH = r"E:\data\webstock\stock_quota"
    #   股票交易详情
    TRADEDETAIL_PATH = r"E:\data\webstock\trade_detail"
    #   dataset数据路径
    DATASET_PATH = r"E:\data\webstock\dataset"
    #   五档交易数据
    TRADEAPPLY_PATH= r"E:\data\webstock\trade_apply\wy"
    # TRADEAPPLY_PATH= r"/root/apply"

    #   股票代码映射表
    # CODEMAPPING_PATH = "static/json/mapping.json"
    #   每日更新的交易详情数据的股票列表
    CODES_PATH = "static/json/codes.json"

    #   网格交易显示时使用的Markline数据
    GRID_MARKLINE_PATH = "static/json/markline"

    #   网格交易数据存储路径
    GRID_PATH = "static/json/grid"


class Configuration():
    #   redis配置
    HOST = "localhost"
    PORT = 6379

    MYSQL_HOST = "localhost"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "123456"
    MYSQL_DB_NAME = "stock"


# =========================
#   网易日线数据字段名称
# =========================
class DailyFieldWY():
    DATE = "DATE"
    CODE = "CODE"
    NAME = "NAME"
    #   收盘价
    TCLOSE = "TCLOSE"
    #   最高价
    HIGH = "HIGH"
    #   最低价
    LOW = "LOW"
    #   开盘价
    TOPEN = "TOPEN"
    #   前收盘价
    LCLOSE = "LCLOSE"
    #   涨跌额
    CHG = "CHG"
    #   涨跌幅
    PCHG = "PCHG"
    #   换手率
    TURNOVER = "TURNOVER"
    #   成交量
    VOTURNOVER = "VOTURNOVER"
    #   成交金额
    VATURNOVER = "VATURNOVER"
    #   总市值
    TCAP = "TCAP"
    #   流通市值
    MCAP = "MCAP"
    #   日线数据csv文件列名与字段对应
    COLUMES={'日期': DATE, '股票代码': CODE, '名称': NAME, '收盘价': TCLOSE, '最高价':HIGH, '最低价': LOW, '开盘价': TOPEN,
             '前收盘': LCLOSE, '涨跌额': CHG, '涨跌幅': PCHG, '换手率': TURNOVER, '成交量': VOTURNOVER, '成交金额': VATURNOVER,
             '总市值': TCAP, '流通市值': MCAP}

    #   交易详情每日统计字段
    #   成交量
    TD_VOTURNOVER_ALL = "TD_VOTURNOVER_ALL"     #   总量
    TD_VOTURNOVER_SELL = "TD_VOTURNOVER_SELL"   #   卖盘
    TD_VOTURNOVER_BUY = "TD_VOTURNOVER_BUY"     #   买盘
    TD_VOTURNOVER_NEUTRAL = "TD_VOTURNOVER_NEUTRAL"  #  中性盘
    #   成交额
    TD_VATURNOVER_ALL = "TD_VATURNOVER_ALL"     #   总量
    TD_VATURNOVER_SELL = "TD_VATURNOVER_SELL"   #   卖盘
    TD_VATURNOVER_BUY = "TD_VATURNOVER_BUY"     #   买盘
    TD_VATURNOVER_NEUTRAL = "TD_VATURNOVER_NEUTRAL" #   中性盘

    #   成交量(小单：交易量在0到100手）)
    TD_VOTURNOVER_VO_0_100_ALL = "TD_VOTURNOVER_VO_0_100_ALL"  # 总量
    TD_VOTURNOVER_VO_0_100_SELL = "TD_VOTURNOVER_VO_0_100_SELL"  # 卖盘
    TD_VOTURNOVER_VO_0_100_BUY = "TD_VOTURNOVER_VO_0_100_BUY"  # 买盘
    TD_VOTURNOVER_VO_0_100_NEUTRAL = "TD_VOTURNOVER_VO_0_100_NEUTRAL"  # 中性盘
    #   成交额(小单：交易量在0到100手）)
    TD_VATURNOVER_VO_0_100_ALL = "TD_VATURNOVER_VO_0_100_ALL"  # 总量
    TD_VATURNOVER_VO_0_100_SELL = "TD_VATURNOVER_VO_0_100_SELL"  # 卖盘
    TD_VATURNOVER_VO_0_100_BUY = "TD_VATURNOVER_VO_0_100_BUY"  # 买盘
    TD_VATURNOVER_VO_0_100_NEUTRAL = "TD_VATURNOVER_VO_0_100_NEUTRAL"  # 中性盘

    #   成交量(中单：交易量在100到1000手）)
    TD_VOTURNOVER_VO_100_1000_ALL = "TD_VOTURNOVER_VO_100_1000_ALL"  # 总量
    TD_VOTURNOVER_VO_100_1000_SELL = "TD_VOTURNOVER_VO_100_1000_SELL"  # 卖盘
    TD_VOTURNOVER_VO_100_1000_BUY = "TD_VOTURNOVER_VO_100_1000_BUY"  # 买盘
    TD_VOTURNOVER_VO_100_1000_NEUTRAL = "TD_VOTURNOVER_VO_100_1000_NEUTRAL"  # 中性盘
    #   成交额(中单：交易量在100到1000手）)
    TD_VATURNOVER_VO_100_1000_ALL = "TD_VATURNOVER_VO_100_1000_ALL"  # 总量
    TD_VATURNOVER_VO_100_1000_SELL = "TD_VATURNOVER_VO_100_1000_SELL"  # 卖盘
    TD_VATURNOVER_VO_100_1000_BUY = "TD_VATURNOVER_VO_100_1000_BUY"  # 买盘
    TD_VATURNOVER_VO_100_1000_NEUTRAL = "TD_VATURNOVER_VO_100_1000_NEUTRAL"  # 中性盘

    #   成交量(大单：交易量在1000手以上）)
    TD_VOTURNOVER_VO_1000_ALL = "TD_VOTURNOVER_VO_1000_ALL"  # 总量
    TD_VOTURNOVER_VO_1000_SELL = "TD_VOTURNOVER_VO_1000_SELL"  # 卖盘
    TD_VOTURNOVER_VO_1000_BUY = "TD_VOTURNOVER_VO_1000_BUY"  # 买盘
    TD_VOTURNOVER_VO_1000_NEUTRAL = "TD_VOTURNOVER_VO_1000_NEUTRAL"  # 中性盘
    #   成交额(大单：交易量在1000手以上）)
    TD_VATURNOVER_VO_1000_ALL = "TD_VATURNOVER_VO_1000_ALL"  # 总量
    TD_VATURNOVER_VO_1000_SELL = "TD_VATURNOVER_VO_1000_SELL"  # 卖盘
    TD_VATURNOVER_VO_1000_BUY = "TD_VATURNOVER_VO_1000_BUY"  # 买盘
    TD_VATURNOVER_VO_1000_NEUTRAL = "TD_VATURNOVER_VO_1000_NEUTRAL"  # 中性盘

    #   成交量(小单：交易额小于10万）)
    TD_VOTURNOVER_VA_0_10_ALL = "TD_VOTURNOVER_VA_0_10_ALL"  # 总量
    TD_VOTURNOVER_VA_0_10_SELL = "TD_VOTURNOVER_VA_0_10_SELL"  # 卖盘
    TD_VOTURNOVER_VA_0_10_BUY = "TD_VOTURNOVER_VA_0_10_BUY"  # 买盘
    TD_VOTURNOVER_VA_0_10_NEUTRAL = "TD_VOTURNOVER_VA_0_10_NEUTRAL"  # 中性盘
    #   成交额(小单：交易额小于10万）)
    TD_VATURNOVER_VA_0_10_ALL = "TD_VATURNOVER_VA_0_10_ALL"  # 总量
    TD_VATURNOVER_VA_0_10_SELL = "TD_VATURNOVER_VA_0_10_SELL"  # 卖盘
    TD_VATURNOVER_VA_0_10_BUY = "TD_VATURNOVER_VA_0_10_BUY"  # 买盘
    TD_VATURNOVER_VA_0_10_NEUTRAL = "TD_VATURNOVER_VA_0_10_NEUTRAL"  # 中性盘

    #   成交量(中单：交易额在10万到100万）)
    TD_VOTURNOVER_VA_10_100_ALL = "TD_VOTURNOVER_VA_10_100_ALL"  # 总量
    TD_VOTURNOVER_VA_10_100_SELL = "TD_VOTURNOVER_VA_10_100_SELL"  # 卖盘
    TD_VOTURNOVER_VA_10_100_BUY = "TD_VOTURNOVER_VA_10_100_BUY"  # 买盘
    TD_VOTURNOVER_VA_10_100_NEUTRAL = "TD_VOTURNOVER_VA_10_100_NEUTRAL"  # 中性盘
    #   成交额(中单：交易额在10万到100万）)
    TD_VATURNOVER_VA_10_100_ALL = "TD_VATURNOVER_VA_10_100_ALL"  # 总量
    TD_VATURNOVER_VA_10_100_SELL = "TD_VATURNOVER_VA_10_100_SELL"  # 卖盘
    TD_VATURNOVER_VA_10_100_BUY = "TD_VATURNOVER_VA_10_100_BUY"  # 买盘
    TD_VATURNOVER_VA_10_100_NEUTRAL = "TD_VATURNOVER_VA_10_100_NEUTRAL"  # 中性盘

    #   成交量(大单：交易额在100万以上）)
    TD_VOTURNOVER_VA_100_ALL = "TD_VOTURNOVER_VA_100_ALL"  # 总量
    TD_VOTURNOVER_VA_100_SELL = "TD_VOTURNOVER_VA_100_SELL"  # 卖盘
    TD_VOTURNOVER_VA_100_BUY = "TD_VOTURNOVER_VA_100_BUY"  # 买盘
    TD_VOTURNOVER_VA_100_NEUTRAL = "TD_VOTURNOVER_VA_100_NEUTRAL"  # 中性盘
    #   成交额(大单：交易额在100万以上）)
    TD_VATURNOVER_VA_100_ALL = "TD_VATURNOVER_VA_100_ALL"  # 总量
    TD_VATURNOVER_VA_100_SELL = "TD_VATURNOVER_VA_100_SELL"  # 卖盘
    TD_VATURNOVER_VA_100_BUY = "TD_VATURNOVER_VA_100_BUY"  # 买盘
    TD_VATURNOVER_VA_100_NEUTRAL = "TD_VATURNOVER_VA_100_NEUTRAL"  # 中性盘


class QuotaField():
    #   macd指标相关
    DIF = "DIF"
    DEA = "DEA"
    MACDHIST = "MACDHIST"
    #   DIF斜率
    DIF_S = "DIF_S"
    DEA_S = "DEA_S"
    MACDHIST_S = "MACDHIST_S"
    #   DIF与DEA的交点
    MACD_CROSS = "MACD_CROSS"

    #   RSI指标相关
    RSI6 = "RSI6"
    RSI6_TYPE = "RSI6_TYPE"
    RSI12 = "RSI12"
    RSI12_TYPE = "RSI12_TYPE"
    RSI24 = "RSI24"
    RSI24_TYPE = "RSI24_TYPE"

    #   ma指标相关
    MA5 = "MA5"
    MA10 = "MA10"
    MA20 = "MA20"
    MA60 = "MA60"
    MA120 = "MA120"
    MA250 = "MA250"
    #   ma5 与ma60的交点
    MA5_60_CROSS = "MA5_60_CROSS"
    #   ma的斜率
    MA5_SLOPE = "MA5_SLOPE"
    MA10_SLOPE = "MA10_SLOPE"

    #   成交量的ma
    VOLUME_MA120 = "VOLUME_MA120"
    #   当日成交量与ma120的交点
    VOLUME_120_CROSS = "VOLUME_120_CROSS"
    #   当日成交量与ma120的差值
    VOLUME_DIFF = "VOLUME_DIFF"

    #   ema
    EMA30 = "EMA30"
    EMA200 = "EMA200"

    #   dmi
    PDI = "PDI"
    MDI = "MDI"
    ADX = "ADX"
    ADXR = "ADXR"
    #   ADX是否大于50
    ADX_TYPE = "ADX_TYPE"
    #   斜率
    PDI_S = "PDI_S"
    MDI_S = "MDI_S"
    #   差值
    PM_DIFF = "PM_DIFF"


class DailyFieldsTushare():
    DATE = "trade_date"
    CODE = "code"
    #   收盘价
    TCLOSE = "close"
    #   最高价
    HIGH = "high"
    #   最低价
    LOW = "low"
    #   开盘价
    TOPEN = "open"
    #   前收盘价
    LCLOSE = "pre_close"
    #   涨跌额
    CHG = "change"
    #   涨跌幅
    PCHG = "pct_chg"
    #   成交量
    VOTURNOVER = "vol"
    #   成交金额
    VATURNOVER = "amount"

    # #   日线数据csv文件列名与字段对应
    # COLUMES={'日期': DATE, '股票代码': CODE,  '收盘价': TCLOSE, '最高价':HIGH, '最低价': LOW, '开盘价': TOPEN,
    #          '前收盘': LCLOSE, '涨跌额': CHG, '涨跌幅': PCHG, '成交量': VOTURNOVER, '成交金额': VATURNOVER}


class DataSetField(DailyFieldsTushare,QuotaField):

    DAILY_DATE="DAILY_DATE"
    DALIY_MISS="DALIY_MISS"
    QUOTA_DATE="QUOTA_DATE"
    QUOTA_MISS="QUOTA_MISS"
    TRADE_DETAIL="TRADE_DETAIL"
    TD_DATE="TD_DATE"
    TD_MISS="TD_MISS"

    KLINE = "KLINE"
    VOLLINE = "VOLLINE"


class HS300Element():
    #   股票代码 +.SH/.SZ
    SECUCODE="SECUCODE"
    #   股票代码
    SECURITY_CODE="SECURITY_CODE"

    TYPE="TYPE"
    #   名称
    SECURITY_NAME_ABBR="SECURITY_NAME_ABBR"
    #   下载时的收盘价
    CLOSE_PRICE = "CLOSE_PRICE"
    #   行业
    INDUSTRY="INDUSTRY"
    #   地区
    REGION="REGION"
    #   推测为权重
    WEIGHT="WEIGHT"
    #   每股收益
    EPS="EPS"
    #   每股净资产
    BPS="BPS"
    #   净资产收益率
    ROE="ROE"
    #   总股本（亿股）
    TOTAL_SHARES="TOTAL_SHARES"
    #   流通股本（亿股）
    FREE_SHARES="FREE_SHARES"
    #   流通市值（亿元）
    FREE_CAP="FREE_CAP"
    F2="f2"
    F3="f3"












