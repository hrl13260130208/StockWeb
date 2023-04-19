

import os
from common.beans import CodeInfo
from common.config import FileConfig
import logging

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

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

        self.infos=[]

        self.load_mapping()


    # def update(self):
    #     """
    #         根据更新的股票列表，来更新股票映射表
    #     :return:
    #     """
    #
    #     self.logger.info("更新股票映射表...")
    #     indexes = {}
    #     code_mapping = {}
    #     symbol_mapping = {}
    #     with open(FileConfig.CODEDETAIL_PATH,"r",encoding="utf-8") as f:
    #         for index, row in enumerate(f.readlines()):
    #             if index == 0:
    #                 continue
    #             items = row.split(",")
    #
    #             indexes[str(index)] = {'code': items[1], 'symbol': items[2]}
    #             code_mapping[items[1]] = str(index)
    #             symbol_mapping[items[2]] = str(index)
    #     path = os.path.join(root_dir, FileConfig.CODEMAPPING_PATH)
    #     with open(path, "w", encoding="utf-8") as f:
    #         json.dump([indexes, code_mapping, symbol_mapping], f)

    def load_mapping(self):
        """
            加载股票映射表
        :return:
        """
        # self.logger.info("加载股票映射表...")
        # path = os.path.join(root_dir,FileConfig.CODEMAPPING_PATH)
        # with open(path, "r", encoding="utf-8") as f:
        #     l = json.load(f)
        #     self.index = l[0]
        #     self.code_mapping = l[1]
        #     self.symbol_mapping = l[2]

        with open(FileConfig.CODEDETAIL_PATH, "r", encoding="utf-8") as f:
            for index, row in enumerate(f.readlines()):
                if index == 0:
                    continue
                items = row.split(",")

                self.index[str(items[0])] = {'code': items[1], 'symbol': items[2]}
                self.code_mapping[items[1]] = str(items[0])
                self.symbol_mapping[items[2]] = str(items[0])
                self.add_info(items)


    def add_info(self,items):
        ci = CodeInfo()
        ci.id=items[0]
        ci.code=items[1]
        ci.symbol=items[2]
        ci.name=items[3]
        ci.area=items[4]
        ci.industry=items[5]
        ci.market=items[6]
        ci.list_date=items[7]
        self.infos.append(ci)


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