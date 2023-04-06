'''
    东方财富 数据源
        下载内容：
            1、沪深300成分股

'''

import os
import requests
import json
import datetime
import pandas as pd
import logging
from common.config import FileConfig
from data.downloader import Downloader

#========================
#   沪深300成分股
#========================
class CodeHS300ElementDownloader(Downloader):

    def __init__(self):
        super(CodeHS300ElementDownloader,self).__init__()
        self.name = "CodeHS300ElementDownloader_" + datetime.datetime.now().strftime("%Y%m%d")
        self.logger = logging.getLogger("CodeHS300ElementDownloader")

    def run(self):
        self.logger.info("开始更新沪深300成分股...")
        url = "http://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112303507602480319112_1632291845673&" \
              "sortColumns=SECURITY_CODE&sortTypes=-1&pageSize=300&pageNumber=1&reportName=RPT_INDEX_TS_COMPONENT&" \
              "columns=SECUCODE%2CSECURITY_CODE%2CTYPE%2CSECURITY_NAME_ABBR%2CCLOSE_PRICE%2CINDUSTRY%2CREGION%2CWEIGHT" \
              "%2CEPS%2CBPS%2CROE%2CTOTAL_SHARES%2CFREE_SHARES%2CFREE_CAP&quoteColumns=f2%2Cf3&source=WEB&client=WEB&" \
              "filter=(TYPE%3D%221%22)"

        resp = requests.get(url)

        string = resp.text
        string = string[42:-2]
        sd = json.loads(string)
        #   字段意义参考：HS300Element
        hs300stocks = pd.DataFrame(columns=['SECUCODE', 'SECURITY_CODE', 'TYPE', 'SECURITY_NAME_ABBR', 'CLOSE_PRICE',
                                            'INDUSTRY', 'REGION', 'WEIGHT', 'EPS', 'BPS', 'ROE', 'TOTAL_SHARES',
                                            'FREE_SHARES', 'FREE_CAP', 'f2', 'f3'])
        for index, d in enumerate(sd["result"]["data"]):
            hs300stocks.loc[index] = d
        filename = "hs300element_"+  datetime.datetime.now().strftime("%Y%m%d") +".csv"
        path = os.path.join(FileConfig.CODEHS300ELEMENT_PATH,filename)
        hs300stocks.to_csv(path, index=False, encoding="utf-8")
        self.logger.info("沪深300成分股更新成功！")


if __name__ == '__main__':
    hs300 = CodeHS300ElementDownloader()
    hs300.run()
