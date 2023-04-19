

import os
import logging
import datetime
import pandas as pd
from shutil import copyfile
from common.config import FileConfig,DailyFieldWY
from data.quota import Quota
from data.tushare_downloader import TradeCalendarDownloader,CodeListDownloader,DailyDownloader
from data.eastmoney_downloader import HS300ElementDownloader


class DataDownloader:
    def __init__(self):
        # 交易日历
        self.calendar=TradeCalendarDownloader()
        # 股票列表
        self.code_list=CodeListDownloader()
        # 日线数据
        self.daily=DailyDownloader()
        # 沪深300成分股
        self.hs300elements=HS300ElementDownloader()
        # 指标
        self.quota= QuotaUpdater()

    def update_calendar(self,end_date):
        self.calendar.download(end_date,save_path=FileConfig.CALENDAR_PATH)

    def update_list(self):
        self.code_list.download("",save_path=FileConfig.CODEDETAIL_PATH)

    def update_daily(self,code):
        path = os.path.join(FileConfig.CODEHISTORY_PATH, code[:code.rfind(".")] + ".csv")
        self.daily.download(code,save_path=path)
        self.quota.update(code[:code.rfind(".")])

    def update_hs300elements(self):
        file = os.path.join(FileConfig.CODEHS300ELEMENT_PATH,"hs300elements.csv")
        filename = "hs300elements_"+  datetime.datetime.now().strftime("%Y%m%d") +".csv"
        path = os.path.join(FileConfig.CODEHS300ELEMENT_PATH,filename)
        copyfile(file,path)
        self.hs300elements.download("",save_path=file)


class QuotaUpdater():
    def __init__(self):
        self.logger = logging.getLogger("QuotaUpdater")
        self.quota = Quota()

    def update(self,code):
        self.logger.debug(f"开始更新股票{code}指标...")
        path = os.path.join(FileConfig.CODEHISTORY_PATH, code + ".csv")
        data = None
        try:
            data = pd.read_csv(path)
        except:
            self.logger.error(f"读取日线数据出处！跳过该股票（{code}）！")
            return

        if len(data) == 0:
            return
        data = data.iloc[::-1]

        try:
            data = self.quota.quota(data)
            file = os.path.join(FileConfig.CODEQUOTA_PATH, code + ".csv")
            data.to_csv(file, index=False, encoding="utf-8")
        except ValueError:
            self.logger.info(f"股票{code}数据不足！")

