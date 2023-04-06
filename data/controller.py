'''
    股票数据下载器
        Controller： 根据当前的数据状况与下载策略，生成下载任务
        executor：   根据下载任务，使用线程池下载数据
'''

import datetime
import logging
from threading import Thread
from data.executor import DownloadExecutor, UpdateExecutor

from utils.trade_calendar import TradeCalendar
from data.data_manager import CodeDetail, CodeMapping
from data.updater import TradeDetailManager
from common.static import Static
from data.dataset import CodeDataSet
from data.downloader import Downloader
import data.datasource_tushare as ts
import data.datasource_eastmoney as em
import data.datasource_wy as wy


class Controller():

    def __init__(self, mapping):
        super(Controller, self).__init__()
        self.logger = logging.getLogger("Controller")
        self.cal = TradeCalendar()
        self.code_detail = CodeDetail()
        self.tdmanager = TradeDetailManager()
        self.tdmanager.load_code()
        self.code_mapping = mapping
        # self.code_mapping.load_mapping()

    def run(self) -> None:

        """
            计划执行需要更新的数据
                1、交易日历
                2、沪深300成分股
                3、股票列表
                4、沪深300历史数据
                5、股票历史数据
                6、成交明细
        :return:
        """

        self.logger.info("开始检查需要下载的数据...")

        today = datetime.datetime.now()
        open_day = self.cal.current_day()
        md = today.strftime("%m%d")
        today_str = today.strftime("%Y%m%d")
        day = today.strftime("%d")

        #   1、检查是否需要更新交易日历
        #       交易日历更新策略：当前日期离日历最大日期不足10日时更新，更新天数30
        self.logger.info("检查交易日历...")
        if self.cal.calender_update():
            self.calender()

        #   2、沪深300成分股 指定日期更新
        #   todo 根据现实沪深300的更新来更新
        self.logger.info("检查沪深300成分股...")
        if md == "0201" or md == "0801":
            self.hs300elements()

        #   3、更新股票列表
        #       每10日更新一次
        self.logger.info("检查股票列表...")
        if int(today_str) % 10 == 0:
            self.stock_list()

        #   4、更新沪深300指标历史数据——每日更新
        self.logger.info("检查沪深300指标历史数据...")
        if self.cal.is_open(today_str):
            self.hs300quota(open_day)

        #   5、更新股票历史数据
        self.logger.info("检查股票历史数据...")
        if day == "01":
            #   每月更新，更新所有股票
            codes = self.code_detail.all_codes()
            self.download_history(codes, open_day)

        else:
            #   其他交易日更新，只更新沪深300
            if self.cal.is_open(today_str):
                codes = self.code_detail.hs300_codes()
                self.download_history(codes, today_str)

        #   6、更新交易详情数据
        self.logger.info("检查交易详情数据...")
        if int(today_str) % 5 == 0:
            all = set(self.code_detail.all_codes())
            downloads = self.tdmanager.check(all=all)
        else:
            downloads = self.tdmanager.check()

        for d in downloads:
            self.trade_detail(d[1], d[0])

        #  更新交易详情数据
        if int(today_str) % 5 == 0:
            update_data = {"file": "data.updater", "fromlist": "data",
                           "class": "TradeDetailManager", "method": "update_codes", }

            d = Downloader()
            d.register(update_data)
            Static.DOWNLOAD_TASKS.put(d)

        #   每月一日将数据更新到dataset中
        if day == "01":
            all_codes = self.code_detail.all_codes()
            cds = CodeDataSet(self.code_mapping)
            for c in all_codes:
                cds.update_code(c)
        self.logger.info("缺失数据检查完成！")

    def download_history(self, codes, date):
        '''
            添加股票历史数据下载任务
        :param codes:
        :param date:
        :return:
        '''
        for c in codes:
            code = self.code_mapping.get_symbol(c)
            update_data = {"file": "data.updater", "fromlist": "data",
                           "class": "QuotaUpdater", "class_args": [code], "method": "update"}

            chd = wy.CodeHistoryDownloader(code, date)
            chd.register(update_data)
            Static.DOWNLOAD_TASKS.put(chd)

    def calender(self):
        '''
            更新交易日历
                更新到下一个月
        :return:
        '''
        self.logger.info("更新交易日历...")
        end = datetime.datetime.now() + datetime.timedelta(days=30)
        end = end.strftime("%Y%m%d")
        tc = ts.TradeCalendarDownloader(end=end)
        Static.DOWNLOAD_TASKS.put(tc)

    def hs300elements(self):
        '''
            更新沪深300成分股
        :return:
        '''
        che = em.CodeHS300ElementDownloader()
        Static.DOWNLOAD_TASKS.put(che)

    def stock_list(self):
        '''
            更新股票列表
        :return:
        '''
        #   更新完成后，同步更新股票映射表
        update_data = {"file": "data.data_manager", "fromlist": "data",
                       "class": "CodeMapping", "method": "update"}
        cdd = ts.CodeListDownloader()
        cdd.register(update_data)
        Static.DOWNLOAD_TASKS.put(cdd)

    def hs300quota(self, open_day):
        '''
            沪深300指标历史数据
        :param open_day:
        :return:
        '''
        chh = wy.CodeHS300HistoryDownloader(open_day)
        Static.DOWNLOAD_TASKS.put(chh)

    def trade_detail(self, code, date):
        update_data = {"file": "data.updater", "fromlist": "data",
                       "class": "TradeDetailManager", "method": "check_download", "method_args": [code, date]}
        tdd = wy.TradeDetailDownloader(code, date)
        tdd.register(update_data)
        Static.DOWNLOAD_TASKS.put(tdd)


