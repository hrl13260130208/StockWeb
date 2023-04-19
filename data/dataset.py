import os
import logging
import pandas as pd

from common.beans import DailyInfo,Hs300ElementInfo
from utils.trade_calendar import TradeCalendar
from common.config import FileConfig

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)
pd.set_option('display.max_rows', None)


# =================================
#   数据集
#       统一数据操作，并提供存储与查询
#           统一数据格式：
#                 交易日历
#                 日线数据
#                 沪深300成分股
# =================================
class CodeDataSet():
    def __init__(self, code_mapping):
        self.logger = logging.getLogger("CodeDataSet")

        # 股票代码映射表
        self.code_mapping = code_mapping
        # 日线数据缓存
        self.cache_data = {}
        # 沪深300成分股 key：股票代码 value：Hs300ElementInfo
        self.hs300_elements={}

        # 交易日历
        self.cal = TradeCalendar()
        self.date_list = []
        self.update_date()


    def update_date(self):
        """
            更新交易日历
        :return:
        """
        self.cal.load_cal()
        start = "20191231"
        self.date_list = self.cal.open_days(start, self.cal.last_date())

    def open_days(self, start_date, end_date):
        '''
            获取指定日期间的开盘日期
        :param start_date:  起始日期
        :param end_date:    结束日期
        :return:
        '''

        return self.cal.open_days(start_date, end_date)

    def current_day(self, start="20191231"):
        '''
            获取指定日期到现在的开盘日期
        :param start:  起始日期
        :return:
        '''
        end = self.cal.current_day()
        return self.open_days(start, end)

    def compute_date(self, date, days=1):
        '''
            计算指定日期后n个开盘日
        :param date:    指定日期
        :param days:    天数（可以为负数，表示前n个开盘日）
        :return:
        '''

        index = self.date_list.index(date)
        if index + days > len(self.date_list):
            raise ValueError("日期超出列表长度")

        start = min(index, index + days)
        end = max(index, index + days)

        return self.date_list[start + 1:end + 1]

    def get_code(self, code):
        """
            获取股票日线数据
                从缓存中获取，若缓存中没有则从磁盘中加载
        :param code:
        :return:
        """
        code_index = self.code_mapping.get_symbol(code)
        if code_index not in self.cache_data.keys():
            if not self.load(code_index):
                raise ValueError(f"无法加载该股票{code_index}！")
        try:
            return self.cache_data[code_index]
        except:
            raise ValueError("无法查询到指定的数据！")

    def klines(self, code, dates):
        """
            查询K线数据
        :param code:
        :param dates:
        :return:
        """
        data = []
        for d in dates:
            data.append(self.kline(code, d))
        return data

    def kline(self, code, date):
        '''
            k线数据（单日）
        :param code:
        :param date:
        :return:
        '''
        codes = self.get_code(code)
        if date in codes.keys():
            data: DailyInfo = self.cache_data[code][date]
            return [data.open, data.close, data.low, data.high]
        else:
            return [0, 0, 0, 0]

    def load(self, code):
        """
            加载股票日线数据到缓存中
        :param code:
        :return:
        """
        #   加载数据
        code = self.code_mapping.get_symbol(code)
        path = self.code_path(code)
        if not os.path.exists(path):
            return False

        code_data = {}
        with open(path, "r", encoding="utf-8") as f:
            for index, row in enumerate(f.readlines()):
                if index == 0:
                    continue
                items = row.split(",")

                ci = DailyInfo()
                ci.id = index
                ci.code = items[0]
                ci.trade_date = items[1]
                ci.open = items[2]
                ci.high = items[3]
                ci.low = items[4]
                ci.close = items[5]
                ci.pre_close = items[6]
                ci.change = items[7]
                ci.pct_chg = items[8]
                ci.vol = items[9]
                ci.amount = items[10]
                code_data[ci.trade_date] = ci

        self.cache_data[code] = code_data

        return True

    def code_path(self, code):
        """
            日线数据路径
        :param code: 股票代码
        :return:
        """
        return os.path.join(FileConfig.CODEHISTORY_PATH, code + ".csv")

    def load_hs300elements(self):
        file = os.path.join(FileConfig.CODEHS300ELEMENT_PATH, "hs300elements.csv")
        with open(file, "r", encoding="utf-8") as f:
            for index, row in enumerate(f.readlines()):
                if index == 0:
                    continue
                items = row.split(",")

                ci = Hs300ElementInfo()
                ci.SECUCODE = items[0]
                ci.SECURITY_CODE = items[1]
                ci.TYPE = items[2]
                ci.SECURITY_NAME_ABBR = items[3]
                ci.CLOSE_PRICE = items[4]
                ci.INDUSTRY = items[5]
                ci.REGION = items[6]
                ci.WEIGHT = items[7]
                ci.EPS = items[8]
                ci.BPS = items[9]
                ci.ROE = items[10]
                ci.TOTAL_SHARES = items[11]
                ci.FREE_SHARES = items[12]
                ci.FREE_CAP = items[13]
                ci.f2 = items[14]
                ci.f3 = items[15]
                self.hs300_elements[ci.SECURITY_CODE] = ci

