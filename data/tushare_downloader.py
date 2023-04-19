'''
    tushare 数据源
        下载内容：
            1、交易日历
            2、股票列表
            3、日线数据

'''
import datetime

import tushare

from common.interface import Downloader

pro = tushare.pro_api("9ba459eb7da2bca7e1827a240a5654bacdf481a1ea997210e049ea91")

start = "20000101"




# ========================
#   交易日历
# ========================
class TradeCalendarDownloader(Downloader):

    def download(self,code,save_path=None):

        df = pro.trade_cal(exchange='', start_date=start, end_date=code)
        if save_path:
            df.to_csv(save_path)

    # def __init__(self, end=None):
    #     super(TradeCalendarDownloader, self).__init__()
    #     self.end = end
    #     self.name = "TradeCalendarDownloader_" + self.end
    #     self.logger = logging.getLogger("TradeCalendarDownloader")
    #     if end == None:
    #         raise ValueError("交易日历结束日期不能为空！")
    #
    # def run(self) -> None:
    #     self.logger.info("下载交易日历数据...")
    #     df = pro.trade_cal(exchange='', start_date=start, end_date=self.end)
    #     df.to_csv(FileConfig.CALENDAR_PATH)
    #     self.logger.info("交易日历更新成功！")


# ========================
#   股票列表
# ========================
class CodeListDownloader(Downloader):

    def download(self,code,save_path=None):

        data = pro.stock_basic()
        if save_path:
            data.to_csv(save_path)

    # def __init__(self):
    #     super(CodeListDownloader, self).__init__()
    #     self.name = "CodeDetailDownloader_" + datetime.datetime.now().strftime("%Y%m%d")
    #     self.logger = logging.getLogger("CodeDetailDownloader")
    #
    # def run(self):
    #     self.logger.info("更新股票列表...")
    #     data = pro.stock_basic()
    #     data.to_csv(FileConfig.CODEDETAIL_PATH)
    #     self.logger.info("股票列表更新完成！")


class DailyDownloader(Downloader):

    def download(self,code,save_path=None):
        df = pro.daily(ts_code=code, end_date=datetime.datetime.now().strftime("%Y%m%d"))
        if save_path:
        # path = os.path.join(FileConfig.CODEHISTORY_PATH,code[:code.rfind(".")]+".csv")
            df.to_csv(save_path,index=False, encoding="utf-8")

if __name__ == '__main__':
    # cd = CodeListDownloader()
    # cd.run()
    # df=pro.daily(ts_code='000783.SZ', start_date='20000101', end_date='20230417')
    # print(df)
    d=DailyDownloader()
    d.download('000783.SZ')