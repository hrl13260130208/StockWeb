

"""
    计算指标
        1、macd
        2、rsi
        3、ma
        4、vol_ma
        5、ema
        6、dmi
"""


import pandas as pd
import talib
from common.config import DataSetField


class Quota():
    def __init__(self):
        pass

    def quota(self, data):
        if len(data)<=250:
            raise ValueError("数据量不足！")
        data = self.macd(data)
        data = self.rsi(data)
        data = self.ma(data)
        data = self.vol_ma(data)
        data = self.ema(data)
        data = self.dmi(data)

        data = data.fillna(value=0)
        return data


    def macd(self,data):
        #   macd
        data.loc[:, DataSetField.DIF], data.loc[:,DataSetField.DEA], data.loc[:,DataSetField.MACDHIST] = \
            talib.MACD(data.loc[:,DataSetField.TCLOSE], fastperiod=12,slowperiod=26, signalperiod=9)
        data.loc[:, "DIF_shift"] =  data.loc[:, DataSetField.DIF].shift(1)
        #   DIF 斜率
        DIF_S = []
        for dif, difs in zip(data.loc[:, "DIF"], data.loc[:, "DIF_shift"]):

            if pd.isna(dif) or pd.isna(difs):
                type = 0
            else:
                d = dif - difs
                if dif > 0:
                    if d > 0:
                        type = 1
                    else:
                        type = 2
                else:
                    if d > 0:
                        type = 3
                    else:
                        type = 4
            DIF_S.append(type)

        data.loc[:, DataSetField.DIF_S] = DIF_S

        #   DEA 斜率
        data.loc[:, "DEA_shift"] =  data.loc[:,DataSetField.DEA].shift(1)
        DEA_S = []
        for dea, deas in zip( data.loc[:,DataSetField.DEA], data.loc[:, "DEA_shift"]):

            if pd.isna(dea) or pd.isna(deas):
                type = 0
            else:
                d = dea - deas
                if dea > 0:
                    if d > 0:
                        type = 1
                    else:
                        type = 2
                else:
                    if d > 0:
                        type = 3
                    else:
                        type = 4
            DEA_S.append(type)

        data.loc[:, DataSetField.DEA_S] = DEA_S

        data.loc[:, "MACDHIST_shift"] = data.loc[:,DataSetField.MACDHIST].shift(1)
        #   MACD斜率
        MACD_S = []
        for macd, macds in zip(data.loc[:,DataSetField.MACDHIST], data.loc[:, "MACDHIST_shift"]):

            if pd.isna(macd) or pd.isna(macds):
                type = 0
            else:
                d = macd - macds
                if macd > 0:
                    if d > 0:
                        type = 1
                    else:
                        type = 2
                else:
                    if d > 0:
                        type = 3
                    else:
                        type = 4
            MACD_S.append(type)
        data.loc[:, "MACDHIST_S"] = MACD_S

        #   DIF与DEA的交点
        CROSS = []
        for dif, dea in zip(data.loc[:, "DIF"], data.loc[:, "DEA"]):
            if pd.isna(dif) or pd.isna(dea):
                type = 0
            elif dif > dea:
                type = 1
            else:
                type = 2
            CROSS.append(type)
        data.loc[:, "MACD_CROSS"] = CROSS

        data = data.drop('DIF_shift', 1)
        data = data.drop('DEA_shift', 1)
        data = data.drop('MACDHIST_shift', 1)
        return data







    def rsi(self,data):

        #   rsi
        data.loc[:, 'RSI6'] = talib.RSI(data.loc[:,DataSetField.TCLOSE], timeperiod=6)
        data.loc[:, 'RSI6_TYPE'] = data.loc[:, 'RSI6'].apply(self.rsi_type)
        data.loc[:, 'RSI12'] = talib.RSI(data.loc[:,DataSetField.TCLOSE], timeperiod=12)
        data.loc[:, 'RSI12_TYPE'] = data.loc[:, 'RSI12'].apply(self.rsi_type)
        data.loc[:, 'RSI24'] = talib.RSI(data.loc[:,DataSetField.TCLOSE], timeperiod=24)
        data.loc[:, 'RSI24_TYPE'] = data.loc[:, 'RSI24'].apply(self.rsi_type)

        return data

    def rsi_type(self,x):
        if pd.isna(x):
            return 0
        elif x < 30:
            return 1
        elif x < 70:
            return 2
        else:
            return 3

    def ma(self,data):
        #   ma
        data.loc[:, 'MA5'] = talib.MA(data.loc[:,DataSetField.TCLOSE], timeperiod=5)
        data.loc[:, 'MA10'] = talib.MA(data.loc[:,DataSetField.TCLOSE], timeperiod=10)
        data.loc[:, 'MA20'] = talib.MA(data.loc[:,DataSetField.TCLOSE], timeperiod=20)
        data.loc[:, 'MA60'] = talib.MA(data.loc[:,DataSetField.TCLOSE], timeperiod=60)
        data.loc[:, 'MA120'] = talib.MA(data.loc[:,DataSetField.TCLOSE], timeperiod=120)
        data.loc[:, 'MA250'] = talib.MA(data.loc[:,DataSetField.TCLOSE], timeperiod=250)

        #   ma5_ma60 cross
        CROSS = []
        for ma5, ma60 in zip(data.loc[:, "MA5"], data.loc[:, "MA60"]):
            if pd.isna(ma5) or pd.isna(ma60):
                type = 0
            elif ma5 > ma60:
                type = 1
            else:
                type = 2
            CROSS.append(type)
        data.loc[:, "MA5_60_CROSS"] = CROSS
        #   ma 斜率
        data.loc[:, "MA5_shift"] = data.loc[:, 'MA5'].shift(1)
        data.loc[:, "MA10_shift"] = data.loc[:, 'MA10'].shift(1)
        data.loc[:, "MA5_SLOPE"] = data.loc[:, 'MA5'] - data.loc[:, "MA5_shift"]
        data.loc[:, "MA10_SLOPE"] = data.loc[:, 'MA10'] - data.loc[:, "MA10_shift"]
        data = data.drop('MA5_shift', 1)
        data = data.drop('MA10_shift', 1)

        return data

    def vol_ma(self,data):
        #   vol ma
        data.loc[:, 'VOLUME_MA120'] = talib.MA(data.loc[:,DataSetField.VOTURNOVER], timeperiod=120)
        #   vol ma cross
        CROSS = []
        DIFF = []
        for vol, vol120 in zip(data.loc[:,DataSetField.VOTURNOVER], data.loc[:, "VOLUME_MA120"]):

            if pd.isna(vol) or pd.isna(vol120):
                type = 0
                diff = 0
            elif vol > vol120:
                type = 1
                diff = vol - vol120
            else:
                type = 2
                diff = vol - vol120
            CROSS.append(type)
            DIFF.append(diff)

        data.loc[:, "VOLUME_120_CROSS"] = CROSS
        data.loc[:, "VOLUME_DIFF"] = DIFF
        return data

    def ema(self,data):

        #   ema
        data.loc[:, "EMA30"] = talib.EMA(data.loc[:,DataSetField.TCLOSE], timeperiod=30)
        data.loc[:, "EMA200"] = talib.EMA(data.loc[:,DataSetField.TCLOSE], timeperiod=200)
        return data

    def dmi(self,data):

        data.loc[:, "PDI"] = talib.PLUS_DI(data.loc[:,DataSetField.HIGH], data.loc[:,DataSetField.LOW], data.loc[:,DataSetField.TCLOSE], timeperiod=7)
        data.loc[:, "MDI"] = talib.MINUS_DI(data.loc[:,DataSetField.HIGH], data.loc[:,DataSetField.LOW], data.loc[:,DataSetField.TCLOSE], timeperiod=7)
        data.loc[:, "ADX"] = talib.ADX(data.loc[:,DataSetField.HIGH], data.loc[:,DataSetField.LOW], data.loc[:,DataSetField.TCLOSE], timeperiod=7)
        data.loc[:, "ADXR"] = talib.ADXR(data.loc[:,DataSetField.HIGH], data.loc[:,DataSetField.LOW], data.loc[:,DataSetField.TCLOSE], timeperiod=14)

        data.loc[:, 'ADX_TYPE'] = data.loc[:, 'ADX'].apply(self.adx_type)

        #   PDI斜率
        PDI_S = []
        data.loc[:, "PDI_shift"] = data.loc[:, "PDI"].shift(1)
        for pdi, pdis in zip(data.loc[:, "PDI"], data.loc[:, "PDI_shift"]):

            if pd.isna(pdi) or pd.isna(pdis):
                type = 0
            else:
                d = pdi - pdis
                if d > 0:
                    type = 1
                else:
                    type = 2

            PDI_S.append(type)
        data.loc[:, "PDI_S"] = PDI_S

        #   MDI斜率
        MDI_S = []
        data.loc[:, "MDI_shift"] = data.loc[:, "MDI"].shift(1)
        for mdi, mdis in zip(data.loc[:, "MDI"], data.loc[:, "MDI_shift"]):

            if pd.isna(mdi) or pd.isna(mdis):
                type = 0
            else:
                d = mdi - mdis
                if d > 0:
                    type = 1
                else:
                    type = 2

            MDI_S.append(type)
        data.loc[:, "MDI_S"] = MDI_S

        #   PDI与MDI差值
        PM_DIFF = []
        for pdi, mdi in zip(data.loc[:, "PDI"], data.loc[:, "MDI"]):

            if pd.isna(pdi) or pd.isna(mdi):
                diff = 0
            else:
                diff = pdi - mdi
            PM_DIFF.append(diff)
        data.loc[:, "PM_DIFF"] = PM_DIFF

        data = data.drop('MDI_shift', 1)
        data = data.drop('PDI_shift', 1)


        return data

    def adx_type(self,x):
        if pd.isna(x):
            return 0
        elif x < 50:
            return 1
        else:
            return 2


