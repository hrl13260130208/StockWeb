'''
    网易财经 数据源
        下载内容：
            1、沪深300历史数据

'''

import os
import requests
import json
import datetime
import pandas as pd
import logging
from common.config import FileConfig
from data.downloader import Downloader,TradeObserver


def gcode(code):
    if code[0] in ["6", "5", "9"]:
        return "0" + code
    elif code[0] in ["0", "1", "2", "3"]:
        return "1" + code
    elif code[0] in ["4","8"]:
        return "2"+code
    else:
        raise ValueError(f"未知的股票{code}！")

# ========================
#   沪深300历史数据
# ========================
class CodeHS300HistoryDownloader(Downloader):

    def __init__(self, end):
        super(CodeHS300HistoryDownloader, self).__init__()
        self.logger = logging.getLogger("CodeHS300HistoryDownloader")
        self.end = end
        self.name = "CodeHS300HistoryDownloader_" + datetime.datetime.now().strftime("%Y%m%d")


    def run(self):
        self.logger.info("下载沪深300指标历史数据...")
        url = f"http://quotes.money.163.com/service/chddata.html?code=0000300&start=20020104&end={self.end}&" \
              f"fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER"
        print(url)
        resp = requests.get(url)
        resp.encoding = "GBK"
        text = resp.text.replace("\r\n", "\n")
        with open(FileConfig.CODEHS300HISTORY_PATH, "w", encoding="utf-8") as f:
            f.write(text)
        self.logger.info("沪深300指标历史数据更新成功！")



# ========================
#   股票历史数据
# ========================
class CodeHistoryDownloader(Downloader):

    def __init__(self, code,end):
        super(CodeHistoryDownloader, self).__init__()
        self.logger = logging.getLogger("CodeHistoryDownloader")
        self.code = code
        self.end = end
        self.name = "CodeHistoryDownloader_" + datetime.datetime.now().strftime("%Y%m%d")+"_"+self.code


    def run(self):
        self.logger.info(f"开始更新股票{self.code}历史数据...")
        code_ = gcode(self.code)
        url = "http://quotes.money.163.com/service/chddata.html?code=%s&start=19900101&end=%s&fields=" \
               "TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP" % (code_, self.end)
        print("url:"+url)
        resp = requests.get(url)
        resp.encoding = "GBK"
        text = resp.text.replace("\r\n", "\n")

        path = os.path.join(FileConfig.CODEHISTORY_PATH,self.code+".csv")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        self.logger.info(f"股票{self.code}历史数据更新成功！")



# ========================
#   股票交易详情数据
# ========================
class TradeDetailDownloader(Downloader):

    def __init__(self, code,date):
        super(TradeDetailDownloader, self).__init__()
        self.logger = logging.getLogger("TradeDetailDownloader")
        self.code = code
        self.date = date
        self.name = "TradeDetailDownloader_" + datetime.datetime.now().strftime("%Y%m%d")+"_"+self.code


    def run(self):
        self.logger.info(f"开始更新股票{self.code}交易详情数据...")
        code_ = gcode(self.code)
        year = self.date[:4]

        url= "http://quotes.money.163.com/cjmx/%s/%s/%s.xls" % (year, self.date, code_)
        self.logger.info(f"股票:{self.code},交易详情数据连接：{url}")
        resp = requests.get(url)

        path = os.path.join(FileConfig.TRADEDETAIL_PATH,self.date+"/"+self.code+".xls")
        with open(path, "wb") as f:
            f.write(resp.content)
        self.logger.info(f"股票{self.code}交易详情数据更新成功！")



# ========================
#   股票实时买卖数据
# ========================
class WYTradeObserver(TradeObserver):

    def get_data(self,codes):
        codes = [ gcode(c) for c in codes]
        codelist=",".join(codes)
        url = f"https://api.money.126.net/data/feed/{codelist},money.api?callback=_ntes_quote_callback95863879"

        resp = requests.get(url)
        jsontext=resp.text[29:-2]
        data =json.loads(jsontext)
        return self.parse_data(data)

    def parse_data(self, data):
        data_new ={}
        for key in data.keys():
            d={}
            data_new[data[key]["symbol"]]=d

            d["code"] = data[key]["symbol"]
            d["name"] = data[key]["name"]
            d["open"] = data[key]["open"]
            d["previous_close"] = data[key]["yestclose"]
            d["current"] = data[key]["price"]
            d["high"] = data[key]["high"]
            d["low"] = data[key]["low"]
            # d["buy_price"] = data[key]["name"]
            # d["sell_price"] = data[key]["name"]
            # d["deal_volume"] = data[key]["name"]
            # d["deal_price"] = data[key]["name"]
            d["buy1_volume"] = data[key]["bidvol1"]
            d["buy1_price"] = data[key]["bid1"]
            d["buy2_volume"] = data[key]["bidvol2"]
            d["buy2_price"] = data[key]["bid2"]
            d["buy3_volume"] = data[key]["bidvol3"]
            d["buy3_price"] = data[key]["bid3"]
            d["buy4_volume"] = data[key]["bidvol4"]
            d["buy4_price"] = data[key]["bid4"]
            d["buy5_volume"] = data[key]["bidvol5"]
            d["buy5_price"] = data[key]["bid5"]
            d["sell1_volume"] = data[key]["askvol1"]
            d["sell1_price"] = data[key]["ask1"]
            d["sell2_volume"] = data[key]["askvol2"]
            d["sell2_price"] = data[key]["ask2"]
            d["sell3_volume"] = data[key]["askvol3"]
            d["sell3_price"] = data[key]["ask3"]
            d["sell4_volume"] = data[key]["askvol4"]
            d["sell4_price"] = data[key]["ask4"]
            d["sell5_volume"] = data[key]["askvol5"]
            d["sell5_price"] = data[key]["ask5"]
            d["date"] = data[key]["time"].split(" ")[0].replace("/","")
            d["time"] = data[key]["time"].split(" ")[1]

        return data_new




if __name__ == '__main__':
    hs300 = TradeDetailDownloader("000981","20220228")
    hs300.run()

    # wyto=WYTradeObserver()
    # wyto.get_data(["601698","000001"])