
import os
import json
import pandas as pd
from common.config import FileConfig,DailyFieldWY
from utils import email_sender
import logging
import traceback
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))



#==================================
#   股票数据详情
#==================================
class CodeDetail():

    def __init__(self):
        self.logger = logging.getLogger("CodeDetail")
        self.code_csv = pd.read_csv(FileConfig.CODEDETAIL_PATH)
        filename = self.hs300element_filename()
        self.hs300element_csv = pd.read_csv(os.path.join(FileConfig.CODEHS300ELEMENT_PATH,filename))
        # self.hs300history_csv = pd.read_csv(FileConfig.CODEHS300HISTORY_PATH)
        # self.hs300history_csv.loc[:,"日期"] = self.hs300history_csv.loc[:,"日期"].apply(lambda x:x.replace("-",""))


    def hs300element_filename(self):
        filename = None
        date = 0
        for file in os.listdir(FileConfig.CODEHS300ELEMENT_PATH):
            if file.startswith("hs300element_"):
                fdate = int(file[13:-4])
                if fdate > date:
                    date = fdate
                    filename = file

        if filename != None:
            return filename
        else:
            raise ValueError("没有找到沪深300成分股文件！")


    def hs300_codes(self):
        """
            沪深300成分股
        :return:
        """
        codes =self.hs300element_csv.loc[:,"SECUCODE"]
        return codes.values

    def all_codes(self):
        """
            股票列表
        :return:
        """
        codes = self.code_csv.loc[:, "ts_code"]
        return codes.values

    def hs300_history(self,date):
        '''
            沪深300历史数据
        :param date:
        :return:
        '''
        d = self.hs300history_csv.loc[self.hs300history_csv["日期"] == date, :]
        return d.values[0]

    def get_daily(self, code, max_date):
        """
            读取日线数据
        :param code:
        :param max_date:
        :return:
        """
        self.logger.info(f"更新股票({code})日线数据...")
        #   读取数据
        path = os.path.join(FileConfig.CODEHISTORY_PATH, code+ ".csv")
        try:
            self.logger.info(f"读取文件：{path}")
            data = pd.read_csv(path)
        except:
            self.logger.error(f"读取日线数据出处！跳过该股票（{code}）！")
            traceback.print_exc()
            email_sender.send_text("异常处理", "日线数据错误", f"无法读取日线数据，日线数据路径：{path}")
            return None
        if len(data) == 0:
            return None
        cdata = data.rename(columns=DailyFieldWY.COLUMES)
        cdata.loc[:, DailyFieldWY.DATE] = cdata.loc[:, DailyFieldWY.DATE].apply(lambda x: int(x.replace("-", "")))

        #   查询指定日期数据，max_date为空则返回所有数据
        if max_date:
            cdata = cdata.loc[cdata.loc[:, DailyFieldWY.DATE] > int(max_date), :]

        if len(cdata) == 0:
            return None
        data = {}

        for index, row in cdata.iterrows():
            d = dict(row)
            date = str(d[DailyFieldWY.DATE])
            del d[DailyFieldWY.DATE]
            del d[DailyFieldWY.CODE]
            data[date] = d

        return data

    def get_quota(self, code, max_date):
        """
            读取股票指标数据
        :param code:
        :param max_date:
        :return:
        """
        #   读取数据
        self.logger.info(f"更新股票({code})指标数据...")
        path = os.path.join(FileConfig.CODEQUOTA_PATH, code + ".csv")
        if not os.path.exists(path):
            return None
        cdata = pd.read_csv(path)

        cdata.loc[:, DailyFieldWY.DATE] = cdata.loc[:, DailyFieldWY.DATE].apply(lambda x: int(x.replace("-", "")))

        #   查询指定日期数据，max_date为空则返回所有数据
        if max_date:
            cdata = cdata.loc[cdata.loc[:, DailyFieldWY.DATE] > int(max_date), :]

        if len(cdata) == 0:
            return None
        data = {}

        for index, row in cdata.iterrows():
            d = dict(row)
            date = str(d[DailyFieldWY.DATE])
            del d[DailyFieldWY.DATE]
            del d[DailyFieldWY.CODE]
            data[date] = d

        return data

    def get_trade_detail(self, code, date):
        """
            读取交易详情数据
        :param code:
        :param date:
        :param download:
        :return:
        """
        self.logger.info(f"更新股票（{code}）在{date}日的交易详情数据...")

        path =  os.path.join(FileConfig.TRADEDETAIL_PATH,date+"/"+code+".xls")

        if not os.path.exists(path):
            return None


        return self.count_trade_detail(path)

    def count_trade_detail(self, path):
        """
            统计指定日期的交易数据
        :param path:
        :return:
        """

        try:
            data = pd.read_excel(path)
        except:
            self.logger.info(f"读取交易详情数据出错，读取文件：{path}")
            email_sender.send_text("异常处理", "交易详情数据错误", f"读取交易详情数据出错，读取文件：{path}")
            return None

        if len(data) == 0:
            return None

        l1 = self.count(data)

        data_vol_0_100 = data.loc[data.loc[:, "成交量（手）"] < 100, ["成交量（手）", "成交额（元）", "性质"]]
        l2 = self.count(data_vol_0_100)

        data_vol_100_1000 = data.loc[data.loc[:, "成交量（手）"] >= 100, ["成交量（手）", "成交额（元）", "性质"]]
        data_vol_100_1000 = data_vol_100_1000.loc[data.loc[:, "成交量（手）"] < 1000, ["成交量（手）", "成交额（元）", "性质"]]
        l3 = self.count(data_vol_100_1000)

        data_vol_1000 = data.loc[data.loc[:, "成交量（手）"] >= 1000, ["成交量（手）", "成交额（元）", "性质"]]
        l4 = self.count(data_vol_1000)

        data_va_10 = data.loc[data.loc[:, "成交额（元）"] < 100000, ["成交量（手）", "成交额（元）", "性质"]]
        l5 = self.count(data_va_10)

        data_va_10_100 = data.loc[data.loc[:, "成交额（元）"] >= 100000, ["成交量（手）", "成交额（元）", "性质"]]
        data_va_10_100 = data_va_10_100.loc[data.loc[:, "成交额（元）"] < 1000000, ["成交量（手）", "成交额（元）", "性质"]]
        l6 = self.count(data_va_10_100)

        data_va_100 = data.loc[data.loc[:, "成交额（元）"] >= 1000000, ["成交量（手）", "成交额（元）", "性质"]]
        l7 = self.count(data_va_100)
        line = {

            DailyFieldWY.TD_VOTURNOVER_ALL: l1[0],
            DailyFieldWY.TD_VOTURNOVER_SELL: l1[1],
            DailyFieldWY.TD_VOTURNOVER_BUY: l1[2],
            DailyFieldWY.TD_VOTURNOVER_NEUTRAL: l1[3],

            DailyFieldWY.TD_VATURNOVER_ALL: l1[4],
            DailyFieldWY.TD_VATURNOVER_SELL: l1[5],
            DailyFieldWY.TD_VATURNOVER_BUY: l1[6],
            DailyFieldWY.TD_VATURNOVER_NEUTRAL: l1[7],

            DailyFieldWY.TD_VOTURNOVER_VO_0_100_ALL: l2[0],
            DailyFieldWY.TD_VOTURNOVER_VO_0_100_SELL: l2[1],
            DailyFieldWY.TD_VOTURNOVER_VO_0_100_BUY: l2[2],
            DailyFieldWY.TD_VOTURNOVER_VO_0_100_NEUTRAL: l2[3],

            DailyFieldWY.TD_VATURNOVER_VO_0_100_ALL: l2[4],
            DailyFieldWY.TD_VATURNOVER_VO_0_100_SELL: l2[5],
            DailyFieldWY.TD_VATURNOVER_VO_0_100_BUY: l2[6],
            DailyFieldWY.TD_VATURNOVER_VO_0_100_NEUTRAL: l2[7],

            DailyFieldWY.TD_VOTURNOVER_VO_100_1000_ALL: l3[0],
            DailyFieldWY.TD_VOTURNOVER_VO_100_1000_SELL: l3[1],
            DailyFieldWY.TD_VOTURNOVER_VO_100_1000_BUY: l3[2],
            DailyFieldWY.TD_VOTURNOVER_VO_100_1000_NEUTRAL: l3[3],

            DailyFieldWY.TD_VATURNOVER_VO_100_1000_ALL: l3[4],
            DailyFieldWY.TD_VATURNOVER_VO_100_1000_SELL: l3[5],
            DailyFieldWY.TD_VATURNOVER_VO_100_1000_BUY: l3[6],
            DailyFieldWY.TD_VATURNOVER_VO_100_1000_NEUTRAL: l3[7],

            DailyFieldWY.TD_VOTURNOVER_VO_1000_ALL: l4[0],
            DailyFieldWY.TD_VOTURNOVER_VO_1000_SELL: l4[1],
            DailyFieldWY.TD_VOTURNOVER_VO_1000_BUY: l4[2],
            DailyFieldWY.TD_VOTURNOVER_VO_1000_NEUTRAL: l4[3],

            DailyFieldWY.TD_VATURNOVER_VO_1000_ALL: l4[4],
            DailyFieldWY.TD_VATURNOVER_VO_1000_SELL: l4[5],
            DailyFieldWY.TD_VATURNOVER_VO_1000_BUY: l4[6],
            DailyFieldWY.TD_VATURNOVER_VO_1000_NEUTRAL: l4[7],

            DailyFieldWY.TD_VOTURNOVER_VA_0_10_ALL: l5[0],
            DailyFieldWY.TD_VOTURNOVER_VA_0_10_SELL: l5[1],
            DailyFieldWY.TD_VOTURNOVER_VA_0_10_BUY: l5[2],
            DailyFieldWY.TD_VOTURNOVER_VA_0_10_NEUTRAL: l5[3],

            DailyFieldWY.TD_VATURNOVER_VA_0_10_ALL: l5[4],
            DailyFieldWY.TD_VATURNOVER_VA_0_10_SELL: l5[5],
            DailyFieldWY.TD_VATURNOVER_VA_0_10_BUY: l5[6],
            DailyFieldWY.TD_VATURNOVER_VA_0_10_NEUTRAL: l5[7],

            DailyFieldWY.TD_VOTURNOVER_VA_10_100_ALL: l6[0],
            DailyFieldWY.TD_VOTURNOVER_VA_10_100_SELL: l6[1],
            DailyFieldWY.TD_VOTURNOVER_VA_10_100_BUY: l6[2],
            DailyFieldWY.TD_VOTURNOVER_VA_10_100_NEUTRAL: l6[3],

            DailyFieldWY.TD_VATURNOVER_VA_10_100_ALL: l6[4],
            DailyFieldWY.TD_VATURNOVER_VA_10_100_SELL: l6[5],
            DailyFieldWY.TD_VATURNOVER_VA_10_100_BUY: l6[6],
            DailyFieldWY.TD_VATURNOVER_VA_10_100_NEUTRAL: l6[7],

            DailyFieldWY.TD_VOTURNOVER_VA_100_ALL: l7[0],
            DailyFieldWY.TD_VOTURNOVER_VA_100_SELL: l7[1],
            DailyFieldWY.TD_VOTURNOVER_VA_100_BUY: l7[2],
            DailyFieldWY.TD_VOTURNOVER_VA_100_NEUTRAL: l7[3],

            DailyFieldWY.TD_VATURNOVER_VA_100_ALL: l7[4],
            DailyFieldWY.TD_VATURNOVER_VA_100_SELL: l7[5],
            DailyFieldWY.TD_VATURNOVER_VA_100_BUY: l7[6],
            DailyFieldWY.TD_VATURNOVER_VA_100_NEUTRAL: l7[7],
        }
        return line

    def count(self, data):
        vol = data.loc[:, "成交量（手）"].sum()
        vol_sell = data.loc[data.loc[:, "性质"] == "卖盘", "成交量（手）"].sum()
        vol_buy = data.loc[data.loc[:, "性质"] == "买盘", "成交量（手）"].sum()
        vol_neutral = data.loc[data.loc[:, "性质"] == "中性盘", "成交量（手）"].sum()

        va = data.loc[:, "成交额（元）"].sum()
        va_sell = data.loc[data.loc[:, "性质"] == "卖盘", "成交额（元）"].sum()
        va_buy = data.loc[data.loc[:, "性质"] == "买盘", "成交额（元）"].sum()
        va_neutral = data.loc[data.loc[:, "性质"] == "中性盘", "成交额（元）"].sum()


        return [int(vol), int(vol_sell), int(vol_buy), int(vol_neutral), float(va), float(va_sell), float(va_buy), float(va_neutral)]

#==============================
#   股票映射表
#==============================
class CodeMapping():
    def __init__(self):
        '''
            映射表
                index ： id--> symbol ,code
                code_mapping ： code --> id
                symbol_mapping : symbol --> id
            symbol : 股票代码（数字）
            code： 股票代码+“。sh或。sz”
        '''

        self.logger = logging.getLogger("CodeMapping")
        self.index = {}
        self.code_mapping = {}
        self.symbol_mapping = {}

        self.load_mapping()


    def update(self):
        """
            根据更新的股票列表，来更新股票映射表
        :return:
        """

        self.logger.info("更新股票映射表...")
        indexes = {}
        code_mapping = {}
        symbol_mapping = {}
        with open(FileConfig.CODEDETAIL_PATH,"r",encoding="utf-8") as f:
            for index, row in enumerate(f.readlines()):
                if index == 0:
                    continue
                items = row.split(",")

                indexes[str(index)] = {'code': items[1], 'symbol': items[2]}
                code_mapping[items[1]] = str(index)
                symbol_mapping[items[2]] = str(index)
        path = os.path.join(root_dir, FileConfig.CODEMAPPING_PATH)
        with open(path, "w", encoding="utf-8") as f:
            json.dump([indexes, code_mapping, symbol_mapping], f)

    def load_mapping(self):
        """
            加载股票映射表
        :return:
        """
        self.logger.info("加载股票映射表...")
        path = os.path.join(root_dir,FileConfig.CODEMAPPING_PATH)
        with open(path, "r", encoding="utf-8") as f:
            l = json.load(f)
            self.index = l[0]
            self.code_mapping = l[1]
            self.symbol_mapping = l[2]

    def get(self, code):

        if code in self.code_mapping.keys():
            return self.code_mapping[code]

        if code in self.symbol_mapping.keys():
            return self.symbol_mapping[code]
        raise ValueError(f"无法找到股票({code})代码！")

    def get_code(self, code):
        i = self.get(code)
        return self.index[i]["code"]

    def get_symbol(self, code):
        i = self.get(code)
        return self.index[i]["symbol"]


if __name__ == '__main__':
    cd = CodeMapping()
    cd.update()
    # cd = CodeDetail()
    # print(cd.hs300_history("20220225"))
