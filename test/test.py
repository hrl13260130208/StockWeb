import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("logger")

from common.mapping import CodeMapping
from tmp.controller import Controller
from tmp.executor import DownloadExecutor, UpdateExecutor


if __name__ == '__main__':

    mapping = CodeMapping()
    c = Controller(mapping)
    d = DownloadExecutor()
    u = UpdateExecutor()

    d.start()
    u.start()

    # c.calender()

    # c.download_history(["000783",],20230208) #无效

    # c.hs300elements()
    # c.stock_list()
    # c.hs300quota("20230208") #无效
    # c.trade_detail("000783","20230208") #无效