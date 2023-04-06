"""
    更新器
        1、股票指标（talib）

"""

import os
import json
import logging
import pandas as pd
from utils import email_sender
from utils.trade_calendar import TradeCalendar
from data.quota import Quota
from common.config import FileConfig, DailyFieldWY


root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# ===================
#   股票指标更新器
# ===================
class QuotaUpdater():
    def __init__(self, code):
        self.logger = logging.getLogger("QuotaUpdater")
        self.code = code
        self.quota = Quota()

    def update(self):
        self.logger.debug(f"开始更新股票{self.code}指标...")
        path = os.path.join(FileConfig.CODEHISTORY_PATH, self.code + ".csv")
        data = None
        try:
            data = pd.read_csv(path)
        except:
            self.logger.error(f"读取日线数据出处！跳过该股票（{self.code}）！")
            email_sender.send_text("异常处理", "日线数据错误", f"无法读取日线数据，股票代码：{self.code}")
            return

        if len(data) == 0:
            return
        data = data.iloc[::-1]
        data = data.rename(columns=DailyFieldWY.COLUMES)
        try:
            data = self.quota.quota(data)
            file = os.path.join(FileConfig.CODEQUOTA_PATH, self.code + ".csv")
            data.to_csv(file, index=False, encoding="utf-8")
        except ValueError:
            self.logger.info(f"股票{self.code}数据不足！")


# ===================
#   股票交易详情数据管理器
# ===================
class TradeDetailManager():

    def __init__(self):
        self.logger = logging.getLogger("TradeDetailManager")
        self.cal = TradeCalendar()
        self.codes = set()

    def update_codes(self):
        """
            更新每日更新的股票交易详情的股票列表
        :return:
        """
        unique = set()
        days = self.cal.current_week()
        for d in days:
            dir = os.path.join(FileConfig.TRADEDETAIL_PATH, d)
            if os.path.exists(dir):
                codes = [c.replace(".xls", "") for c in os.listdir(dir)]
                unique.update(codes)
        path = os.path.join(root_dir, FileConfig.CODES_PATH)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(list(unique), f)

    def load_code(self):
        path = os.path.join(root_dir, FileConfig.CODES_PATH)
        with open(path, "r", encoding="utf-8") as f:
            self.codes = set(json.load(f))

    def check(self,all=None):
        """
            检查文件，确认需要下载的交易数据
        :return:
        """
        days = self.cal.current_week()
        data = []
        for index, d in enumerate(days):
            dir = os.path.join(FileConfig.TRADEDETAIL_PATH, d)
            if os.path.exists(dir):
                codes = [c.replace(".xls", "") for c in os.listdir(dir)]
                unique = set(codes)
                if index == 1 and all !=None:
                    loss = all - unique
                else:
                    loss = self.codes - unique
                if index == 0 and len(loss) > 0:
                    email_sender.send_text("异常处理", "交易详情数据缺失", f"缺失日期：{d}\n 缺失股票代码：{loss}")
                data.extend([(d, c) for c in loss])

            else:
                os.mkdir(dir)
                data.extend([(d, c) for c in self.codes])
        return data

    def check_download(self,code,date):
        """
            检查下载文件完整性
        :param code:
        :param date:
        :return:
        """
        path = os.path.join(FileConfig.TRADEDETAIL_PATH, date+"/"+code+".xls")
        self.logger.debug(f"开始检查文件({path})完整性...")
        if os.path.exists(path):
            sz = os.path.getsize(path)
            if sz < 6 * 1024:
                self.logger.info(f"文件小于指定大小，删除该文件：{path}")
                os.remove(path)




if __name__ == '__main__':
    tdm = TradeDetailManager()
    # tdm.update_codes()
    tdm.load_code()
    print(tdm.check())
