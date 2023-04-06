'''
    下载任务接口
'''

from common.static import Static


class Downloader():
    def __init__(self):
        self.update_list = []
        self.name = "Downloader"

    def register(self, data):
        """
            注册需要在下载完数据后，立马更新的任务

        :param data: 描述更新任务的数据，数据类型为字典，格式如下{"file":"utils.code_detail","fromlist":"utils",
                        "class":"CodeMapping","class_args":["xx","xx"],"method":"update","method_args":["xx","xx"]}
        :return:
        """
        self.update_list.append(data)

    def run(self):
        pass

    def start(self):
        self.run()
        for data in self.update_list:
            Static.UPDATE_TASKS.put(data)


class TradeObserver():

    def get_data(self, codes):
        """
            获取实时买卖的详情数据

        :param codes: 需要监控的股票列表
        :return:    包含具体股票信息的字典
        """
        pass

    def parse_data(self, data):
        """
            解析数据，并将其转换为统一格式
        :param text:
        :return:
        """
        # d = {}
        # text = text.strip()
        # text = text[text.find("\"") + 1:-2]
        #
        # items = text.split(",")
        # d["name"] = items[0]
        # d["open"] = items[1]
        # d["previous_close"] = items[2]
        # d["current"] = items[3]
        # d["high"] = items[4]
        # d["low"] = items[5]
        # d["buy_price"] = items[6]
        # d["sell_price"] = items[7]
        # d["deal_volume"] = items[8]
        # d["deal_price"] = items[9]
        # d["buy1_volume"] = items[10]
        # d["buy1_price"] = items[11]
        # d["buy2_volume"] = items[12]
        # d["buy2_price"] = items[13]
        # d["buy3_volume"] = items[14]
        # d["buy3_price"] = items[15]
        # d["buy4_volume"] = items[16]
        # d["buy4_price"] = items[17]
        # d["buy5_volume"] = items[18]
        # d["buy5_price"] = items[19]
        # d["sell1_volume"] = items[20]
        # d["sell1_price"] = items[21]
        # d["sell2_volume"] = items[22]
        # d["sell2_price"] = items[23]
        # d["sell3_volume"] = items[24]
        # d["sell3_price"] = items[25]
        # d["sell4_volume"] = items[26]
        # d["sell4_price"] = items[27]
        # d["sell5_volume"] = items[28]
        # d["sell5_price"] = items[29]
        # d["date"] = items[30]
        # d["time"] = items[31]
        # return d
