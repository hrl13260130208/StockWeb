import logging

import tushare
import pandas as pd
import redis
import json
import datetime

import os
from queue import Queue

from common.config import DataSetField
from utils import utils
from utils.trade_calendar import TradeCalendar
from data.data_manager import CodeDetail,CodeMapping
from common.config import FileConfig,Configuration

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)
pd.set_option('display.max_rows', None)


# =================================
#   数据集
#       统一数据格式，并提供存储与查询
#           统一数据格式：{code:{date:{key:value}}}
#           可配置数据来源（DataSource）：
#               数据来源需要实现以下功能：
#                   更新：
#                       dataset会按日按股票进行更新，要求返回对应的数据
#           数据存储：
#               json格式，一只股票一个文件
# =================================
class CodeDataSet():
    def __init__(self,code_mapping):
        self.logger = logging.getLogger("CodeDataSet")

        self.max_cache_code = 250
        self.cache_code = Queue(maxsize=self.max_cache_code)
        self.cache_data = {}

        self.cal = TradeCalendar()
        self.code_detail =  CodeDetail()


        self.code_mapping = code_mapping


        self.r = redis.Redis(host=Configuration.HOST, port=Configuration.PORT)

        start="20101231"
        self.date_list = self.cal.open_days(start, self.cal.last_date())

        # self.pro = tushare.pro_api("9ba459eb7da2bca7e1827a240a5654bacdf481a1ea997210e049ea91")

        # hs300_data = pd.read_csv(self.config.HS300_DATA_PATH)
        # hs300_data["trade_date"] = hs300_data["trade_date"].astype(str)
        # self.hs300_data = hs300_data.fillna(value=0)





    def get_days(self, start_date, end_date):
        '''
            获取开盘日期
        :param start_date:
        :param end_date:
        :return:
        '''

        return self.cal.open_days(start_date, end_date)
    #
    def compute_date(self, date, days=1):
        '''
            计算日期
        :param end_date:
        :param days:
        :return:
        '''

        index = self.date_list.index(date)
        if index+days>len(self.date_list):
            raise ValueError("日期超出列表长度")

        start = min(index,index+days)
        end = max(index,index+days)

        return self.date_list[start+1:end+1]

    def get(self, code, date):
        '''
            获取指定日期的数据

        :param code:
        :param date:
        :return:
        '''
        code_index = self.code_mapping.get_symbol(code)
        if code_index not in self.cache_data.keys():
            if not self.load(code_index):
                raise ValueError(f"无法加载该股票{code_index}！")
        try:
            return self.cache_data[code_index][date]
        except:
            raise ValueError("无法查询到指定的数据！")

    def get_echarts_data(self, code, start, key):

        '''
            web 页面使用，查询页面展示需要的代码
        :param code:
        :param start:
        :param key:
        :return:
        '''


        code = self.code_mapping.get_symbol(code)
        end = self.cal.current_day()
        dlist=self.date_list[self.date_list.index(start):self.date_list.index(end)+1]
        if key == DataSetField.DATE:
            return dlist
        else:
            return self.echarts_data(code,dlist,key)

    def get_label_data(self,code,start):
        futures=self.label_data(code,start,days=5)
        previous = self.label_data(code,start,days=-5)
        return [previous,futures]

    def label_data(self,code,start,days=5):
        code = self.code_mapping.get_symbol(code)
        future=self.compute_date(start,days)
        lines=self.echarts_data(code,future,DataSetField.KLINE)
        return {DataSetField.DATE:future,DataSetField.KLINE:lines}


    def echarts_data(self,code,dates,key):
        '''
            解析echarts需要的数据
        :param code:
        :param dates:
        :param key:
        :return:
        '''
        if code not in self.cache_data.keys():
            if not self.load(code):
                raise ValueError(f"无法加载该股票{code}！")

        data = []
        for d in dates:
            if key == DataSetField.KLINE:
                sd = self.kline(code,d)
            elif key == DataSetField.VOLLINE:
                sd = self.volline(code,d)

            else:
                sd= self.commonline(code, d, key)
            data.append(sd)
        return data

    def kline(self,code,date):
        '''
            k线数据
        :param code:
        :param date:
        :return:
        '''
        if date in self.cache_data[code].keys():
            return  [self.cache_data[code][date][DataSetField.TOPEN],
                   self.cache_data[code][date][DataSetField.TCLOSE],
                   self.cache_data[code][date][DataSetField.LOW],
                   self.cache_data[code][date][DataSetField.HIGH]]
        else:
            return [0,0,0,0]

    def volline(self,code,date):
        """
            成交量数据
        :param code:
        :param date:
        :return:
        """
        if date in self.cache_data[code].keys():
            if self.cache_data[code][date][DataSetField.TOPEN] > self.cache_data[code][date][DataSetField.TCLOSE]:
                s_vol = {"value": self.cache_data[code][date][DataSetField.VOTURNOVER], "itemStyle": {"color": '#00da3c'}}
            else:
                s_vol = {"value": self.cache_data[code][date][DataSetField.VOTURNOVER], "itemStyle": {"color": '#ec0000'}}
        else:
            s_vol = {"value": 0, "itemStyle": {"color": '#ec0000'}}

        return s_vol

    def commonline(self,code,date,key):
        if date in self.cache_data[code].keys():
            if key in  self.cache_data[code][date].keys():
                sd = self.cache_data[code][date][key]
            else:
                sd = 0
        else:
            sd = 0

        return sd


    def hs300_redis(self, code):
        """
            从redis获取数据
        :param code:
        :param key:
        :return:
        """

        result = {}
        code_index = self.code_mapping.get(code)
        for key in self.r.hkeys(code_index):
            value = self.r.hget(code_index, key)
            if value == None:
                value = []
            else:
                value = json.loads(value)
            result[str(key, encoding="utf-8")] = value
        return result

    def load_hs300(self):
        df_hs300 = pd.read_csv(self.config.HS300_PATH, encoding="GBK")
        df_hs300["日期"] = df_hs300["日期"].apply(lambda x: x.replace('-', ""))
        self.df_hs300 = df_hs300

    def hs300(self, date):
        '''
            沪深300历史数据
         日期     股票代码     名称      收盘价      最高价      最低价      开盘价      前收盘   涨跌额     涨跌幅  成交量  成交金额
        :param date:
        :return:
        '''

        return self.code_detail.hs300_history(date)


    def hs300_code(self):
        '''
            返回沪深300
        :return:
        '''
        return self.code_detail.hs300_codes()




    def load(self, code):
        """
            加载数据
        :param code:
        :return:
        """
        #   缓存满了，清除最开始加载的10%的数据
        if self.cache_code.qsize() >= self.max_cache_code-5:
            codes = [self.cache_code.get() for i in range(self.max_cache_code // 10)]
            self.logger.info(f"缓存数据过多，清除数据：{codes}")
            for c in codes:
                del self.cache_data[c]

        #   加载数据
        code = self.code_mapping.get_symbol(code)
        path = self.code_path(code)
        if not os.path.exists(path):
            return False
        with open(path, "r") as f:
            self.cache_data[code] = json.load(f)
            self.cache_code.put(code)
        # try:
        #     with open(path, "r") as f:
        #         self.cache_data[code] = json.load(f)
        #         self.cache_code.put(code)
        # except:
        #     return False
        return True

    def save(self, code):
        """
            保存股票
        :param code:
        :return:
        """
        code = self.code_mapping.get_symbol(code)
        if code not in self.cache_data.keys():
            self.logger.info("未找到该股票，跳过存储！")
            return
        path = self.code_path(code)
        with open(path, "w") as f:
            json.dump(self.cache_data[code], f,cls=utils.NpEncoder)

    def code_path(self, code):
        return os.path.join(FileConfig.DATASET_PATH, code + ".json")

    def update_code(self, code):
        """
            更新股票数据
                日线数据
                指标数据
                交易详情统计数据
        :param code:
        :return:
        """
        code = self.code_mapping.get_symbol(code)
        self.logger.info(f"更新DataSet数据，股票代码：{code}...")

        if code in self.cache_data.keys():
            code_data = self.cache_data[code]
        else:
            load = self.load(code)
            if load:
                code_data = self.cache_data[code]
            else:
                code_data = self.init_code(code)

        #   更新日线
        data = self.code_detail.get_daily(code, code_data[DataSetField.DAILY_DATE])
        if data != None:
            self.update_dict(code, DataSetField.DAILY_DATE, data)

        #   更新指标数据
        data = self.code_detail.get_quota(code, code_data[DataSetField.QUOTA_DATE])
        if data != None:
            self.update_dict(code, DataSetField.QUOTA_DATE, data)

        #   更新交易详情
        self.get_trade_detail(code)

        #   保存数据
        self.save(code)



    def get_trade_detail(self, code):
        '''
            更新交易详情数据
        :param code:
        :return:
        '''
        today = datetime.datetime.now().strftime("%Y%m%d")
        update_list = self.cal.open_days(self.cache_data[code][DataSetField.TD_DATE],today)

        #   更新数据
        for date in update_list:
            data = self.code_detail.get_trade_detail(code, date)
            if data != None:

                if date in  self.cache_data[code].keys():
                    self.cache_data[code][date].update(data)
                else:
                    self.cache_data[code][date] = data

                self.cache_data[code][DataSetField.TD_DATE] = today

    def init_code(self, code):

        self.cache_data[code] = {}

        d = {
            DataSetField.DAILY_DATE: None,
            DataSetField.QUOTA_DATE: None,
            DataSetField.TRADE_DETAIL: False,
            DataSetField.TD_DATE: "20211105",
            DataSetField.TD_MISS: []
        }
        self.cache_data[code].update(d)
        self.save(code)
        self.load(code)
        return d

    def update_dict(self, code, type, data):
        max = 0
        for k in data.keys():
            ik = int(k)
            if ik > max:
                max = ik

            if k in self.cache_data[code].keys():
                self.cache_data[code][k].update(data[k])
            else:
                self.cache_data[code][k] = data[k]
        if max != 0:
            self.cache_data[code][type] = str(max)

    def update_all(self):
        a = {k for k in self.code_mapping.symbol_mapping.keys()}

        for c in a:
            self.update_code(c)

if __name__ == '__main__':
    # conf = Config()
    cds = CodeDataSet()
    cds.update_code("601698")

    # cds.update_hs300data_csv()
    # cds.update_hs300_basic_mysql()
    # cds.update_hs300data()
    # cds.init_mysql()
