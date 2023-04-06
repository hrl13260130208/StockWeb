# from config import Config
from common.config import FileConfig
# import talib
import os
import json
import numpy as np

root_dir = os.path.abspath(os.path.dirname(__file__))

def save_asset(DF_ASSET, d, remain_cash, code_cash):
    DF_ASSET.loc[d] = {
        "total": round(remain_cash + code_cash, 2),
        "cash": round(remain_cash, 2),
        "codes": round(code_cash, 2),
        "cash_percent": round(remain_cash / (remain_cash + code_cash), 2)
    }


# def save_profit(DF_PROFIT, d, total, hs300_value, hs300_start):
#     # print("--------------------",type(total),total)
#     DF_PROFIT.loc[d] = {
#         "net_value": round(total / Config.INIT_CASH, 2),
#         "profit": round(100 * (total - Config.INIT_CASH) / Config.INIT_CASH, 2),
#         "hs300": round(100 * (hs300_value - hs300_start) / hs300_start, 2),
#         "total": float(total)
#     }


def check_cross(line1, line2):
    '''
        判断两条线是否交叉，需要三个点
    :param line1: [a,b,c]  a 前两天 b 前一天 c 当天
    :param line2:
    :return:    1：代表line1上穿line2 -1：代表line1下穿line2 0：没有交叉
    '''

    previous2 = line1[0] - line2[0]
    previous1 = line1[1] - line2[1]
    after = line1[2] - line2[2]
    if previous1 == 0:
        #   交点正好在前一天
        if previous2 < 0 and after > 0:
            return 1
        elif previous2 > 0 and after < 0:
            return -1
        else:
            return 0

    else:
        if previous1 < 0 and after > 0:
            return 1
        elif previous1 > 0 and after < 0:
            return -1
        else:
            return 0






def grid_markline_path(code):
    return os.path.join(root_dir,FileConfig.GRID_MARKLINE_PATH + "_" + code + ".json")


d = {"<class 'str'>": "varchar(200)", "<class 'numpy.int64'>": "bigint", "<class 'numpy.float64'>": "double"}


def create_sql(table_name, feilds):
    s = ",".join([f"`{f}` {d[feilds[f]]} " for f in feilds])
    sql2 = f"CREATE TABLE `{table_name}`  (`id` char(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '主键'," \
           "`code` char(6) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '股票代码'," \
           "`date` date NOT NULL COMMENT '日期'," + s + ") ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;"
    print(sql2)



class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)



if __name__ == '__main__':
    pass
