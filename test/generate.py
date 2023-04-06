import pymysql
import json
from pymysql.cursors import DictCursor

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='webstock')

cursor = connection.cursor(cursor=DictCursor)
cursor.execute(f"SELECT id,date,price,num,pair_id FROM trade_line WHERE  code=000783")
buy = cursor.fetchall()

path = r"E:\File\workspace\python\StockBacktest\data\time_price_000783.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

markpoint = {}
for i in buy:
    # print(i)
    # ["20220609", "09:32:24", 5.78, 2000, 0],
    # i["price"]
    if i["date"] in data.keys():
        if i["date"] in markpoint.keys():
            mp = markpoint[i["date"]]
        else:
            mp = []
            markpoint[i["date"]] = mp
        if (i["num"] > 0):
            for j in data[i["date"]]:
                if j[1] < i["price"]:
                    if i["pair_id"] == None:
                        mp.append([i["date"], j[0], i["price"], i["num"], 0])
                    else:
                        mp.append([i["date"], j[0], i["price"], i["num"], 1])
                    break

        else:
            last = 1
            for j in data[i["date"]]:
                if j[1] > i["price"]:
                    if i["pair_id"] == None:
                        mp.append([i["date"], j[0], i["price"], i["num"], 2])
                    else:
                        mp.append([i["date"], j[0], i["price"], i["num"], 3])
                    break

with open(r"E:\File\workspace\python\StockBacktest\data/logs/markpoint.json", "w", encoding="utf-8") as f:
    json.dump(markpoint, f)
print(markpoint)
