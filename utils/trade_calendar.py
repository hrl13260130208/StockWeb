
"""
    交易日历
"""

import datetime
import os
import pandas as pd
from common.config import FileConfig


class TradeCalendar():

    def __init__(self):
        if os.path.exists(FileConfig.CALENDAR_PATH):
            self.cal = pd.read_csv(FileConfig.CALENDAR_PATH)
            self.cal.loc[:, ["cal_date", "pretrade_date"]] = self.cal.loc[:, ["cal_date", "pretrade_date"]].astype(str)
        else:
            self.cal = None

    def calender_update(self):
        """
            判断是否需要更新日历
        :return:
        """

        if not isinstance(self.cal, pd.DataFrame):
            return True
        today = datetime.datetime.now()
        today = today.strftime("%Y%m%d")

        line = self.cal.loc[self.cal.loc[:, "cal_date"] == today, :].index
        if len(self.cal) - line[0] < 10:
            return True
        else:
            return False

    def current_day(self):
        """
            查询当前最新的交易日期
        :return:
        """

        today = datetime.datetime.now()
        today = today.strftime("%Y%m%d")
        if self.is_open(today):
            return today

        line = self.cal.loc[self.cal.loc[:, "cal_date"] == today, :]
        if len(line) == 1:
            return line.loc[:, "pretrade_date"].values[0]
        else:
            raise ValueError("无法查询当前日期！")

    def is_open(self,date):
        line = self.cal.loc[self.cal.loc[:, "cal_date"] == date, :]
        if len(line) == 1:
            return line.loc[:, "is_open"].values[0]
        else:
            raise ValueError("无法查询当前日期！")


    def current_week(self):
        """
            最近一周的交易日
        :return:
        """
        today = datetime.datetime.now()
        start = today-datetime.timedelta(days=6)
        today = today.strftime("%Y%m%d")
        start = start.strftime("%Y%m%d")

        return self.open_days(start,today)

    def open_days(self,start,end):
        start_index = self.cal.loc[self.cal.loc[:, "cal_date"] == start, :].index
        end_index = self.cal.loc[self.cal.loc[:, "cal_date"] == end, :].index
        start_index = start_index.values[0]
        end_index = end_index.values[0]
        data = self.cal.loc[start_index:end_index, :]
        data = data.loc[data.loc[:, "is_open"] == 1, "cal_date"]
        return [d for d in data.values]

    def last_date(self):
        return self.cal.loc[:,"cal_date"].values[-1]






if __name__ == '__main__':
    t=TradeCalendar()
    print(t.last_date())




