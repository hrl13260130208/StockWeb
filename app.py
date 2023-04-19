import logging
import os
import warnings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("logger")
from flask import Flask
from flask import request
import json

from common.config import FileConfig, DataSetField
from common.mapping import CodeMapping

from tables import *
import easyocr
import uuid
from data.dataset import CodeDataSet
from data.downloader import DataDownloader

import datetime
import pymysql
from utils.email_sender import send_text
from pymysql.cursors import DictCursor

# 打开数据库连接
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='webstock')

mapping = CodeMapping()
cds = CodeDataSet(mapping)

reader = easyocr.Reader(['ch_sim', 'en'])  # 只需要运行一次就可以将模型加载到内存中

downloader = DataDownloader()

app = Flask(__name__, template_folder="static/html")
# 连接数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/webstock'
# 设置是否跟踪数据库的修改情况，一般不跟踪
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 数据库操作时是否显示原始SQL语句，一般都是打开的，因为我们后台要日志
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

label_datas = []


@app.route('/codejosn', methods=["get"])
def code_json():
    '''
        查询日线即指标数据
    :return:
    '''
    code = request.args['code']
    code = mapping.get_symbol(code)

    r = get_kline(code)
    return r


def get_kline(code):
    start = "20191231"
    r = {}
    days = cds.current_day(start=start)
    r[DataSetField.DATE] = days
    r[DataSetField.KLINE] = cds.klines(code, days)

    # r[DataSetField.DATE] = cds.get_echarts_data(code, start, DataSetField.DATE)
    # r[DataSetField.KLINE] = cds.get_echarts_data(code, start, DataSetField.KLINE)
    # r[DataSetField.MA5] = cds.get_echarts_data(code, start, DataSetField.MA5)
    # r[DataSetField.EMA30] = cds.get_echarts_data(code, start, DataSetField.EMA30)
    # r[DataSetField.EMA200] = cds.get_echarts_data(code, start, DataSetField.EMA200)
    # r[DataSetField.MA60] = cds.get_echarts_data(code, start, DataSetField.MA60)
    # r[DataSetField.MA250] = cds.get_echarts_data(code, start, DataSetField.MA250)

    return r


def trade_line_grid(code):
    '''
        真实的买卖信息，封装成echarts k线图上的买卖点
    :param code:
    :return:
    '''
    # 使用 cursor() 方法创建一个游标对象 cursor
    connection.ping()
    cursor = connection.cursor(cursor=DictCursor)
    cursor.execute(f"SELECT * FROM trade_line WHERE code={code} order by date")
    markpoint = []
    for i in cursor.fetchall():
        data = {"coord": [i["date"], i["price"]],
                "value": i["type"][0],
                "itemStyle": {"color": 'rgb(193,4,4)' if i["type"] == "买入" else 'rgb(28,134,4)'}
                }
        markpoint.append(data)
    return markpoint


@app.route('/partline/<code>/<start>')
def partline(code, start):
    echarts = cds.get_label_data(code, start)

    data = {
        "next": echarts[1][DataSetField.DATE][0]
        , "high": echarts[1][DataSetField.KLINE][0][3]
        , "low": echarts[1][DataSetField.KLINE][0][2]
        , "open": echarts[1][DataSetField.KLINE][0][0]
        , "nextclose": echarts[1][DataSetField.KLINE][0][1]
        , "code": code
        , "close": echarts[0][DataSetField.KLINE][-1][1]
        , "previous": echarts[0]
        , "future": echarts[1]
        , "current": start
        , "last": echarts[0][DataSetField.DATE][-2]
    }
    return data


@app.route('/labeldata', methods=["post"])
def labeldata():
    code = request.form.get("code")
    listDate = request.form.get("listDate")
    date = request.form.get("date")
    type = request.form.get("type")
    high = request.form.get("high")
    low = request.form.get("low")
    open = request.form.get("open")
    nextClose = request.form.get("nextClose")
    close = request.form.get("close")
    label = [code, date, type, high, low, open, nextClose, close, listDate[1:]]
    print(label)
    label_datas.append(label)

    return "oK"


@app.route('/save')
def save():
    file_name = uuid.uuid4().__str__().replace("-", "")
    with open("./static/temp/" + file_name + ".txt", "w", encoding="utf-8") as f:
        for i in range(len(label_datas)):
            data = label_datas.pop()
            f.write(",".join(data) + "\n")

    return "ok"


@app.route('/upload_image', methods=["post"])
def upload_image():
    '''
        识别交易详细图片
    :return:
    '''
    image = request.files.get("trade")
    suffix = image.filename.split(".")[-1]
    name = uuid.uuid4().__str__().replace("-", "")
    path = os.path.join("static/image", name + "." + suffix)

    image.save(path)

    result = reader.readtext(path)
    key = ["日期", "股票名称", "买卖方向", "成交数量", "成交价格", "成交金额", "股票代码", "手续费", "印花税", "过户费", "发生金额", "委托号", "摘要"]
    line = {"path": path}
    lv = [r[1] for r in result]
    for index, r in enumerate(lv):
        if r in key:
            line[r] = lv[index + 1]
        elif "手续费" in r:
            line["手续费"] = lv[index + 1]
    return line


@app.route('/insert/trade', methods=["post"])
def insert_trade():
    '''
        保存交易数据
    :return:
    '''
    data = request.json

    data["grid"] = True if int(data["grid"]) else False
    data["year"] = data["date"][:4]
    data["month"] = data["date"][4:6]

    logger.info(f"访问接口：/insert/trade，传入数据：{data}")
    tl = db.session.query(TradeLine).filter(TradeLine.date == data["date"],
                                            TradeLine.tradeNum == data["tradeNum"])
    tlf = tl.all()
    if (len(tlf) == 0):
        new_tl = TradeLine()
        new_tl.date = data["date"]
        new_tl.name = data["name"]
        new_tl.type = data["type"]
        new_tl.num = data["num"]
        new_tl.price = data["price"]
        new_tl.amount = data["amount"]
        new_tl.code = data["code"]
        new_tl.cost = data["cost"]
        new_tl.tax = data["tax"]
        new_tl.transferCost = data["transferCost"]
        new_tl.realAmount = data["realAmount"]
        new_tl.tradeNum = data["tradeNum"]
        new_tl.summary = data["summary"]
        new_tl.grid = data["grid"]
        new_tl.gridPrice = data["gridPrice"]
        new_tl.year = data["year"]
        new_tl.month = data["month"]
        new_tl.strategy = data["strategy"]

        db.session.add(new_tl)
        db.session.commit()
    else:
        tl.update(data)

    return "ok"


@app.route('/daily/detail', methods=["get"])
def daily_detail():
    code = request.args["code"]
    date = request.args["date"]

    path = os.path.join(FileConfig.TRADEAPPLY_PATH, date + ".txt")
    code = mapping.get_symbol(code)
    datas = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.replace("\n", "")
            d = json.loads(line)
            c = mapping.get_symbol(d["code"])
            if c == code:
                datas.append(d)

    datas = sorted(datas, key=lambda x: x["time"])
    return json.dumps(datas)


@app.route('/trade/line', methods=["get"])
def trade_line():
    '''
        获取网格交易中待成交的数据
    :return:
    '''
    code = request.args["code"]
    print(code)
    code = mapping.get_symbol(code)
    # 使用 cursor() 方法创建一个游标对象 cursor
    connection.ping()
    cursor = connection.cursor(cursor=DictCursor)
    cursor.execute(
        f"SELECT id,date,name,price,num,realAmount,gridPrice FROM trade_line WHERE grid=1 AND code={code} AND type='买入' ORDER BY price")
    print(
        f"SELECT id,date,name,price,num,realAmount,gridPrice FROM trade_line WHERE grid=1 AND code={code} AND type='买入' ORDER BY price")
    buy = cursor.fetchall()
    cursor.execute(
        f"SELECT id,date,name,price,num,realAmount,gridPrice FROM trade_line WHERE grid=1 AND code={code} AND type='卖出' ORDER BY price")
    sell = cursor.fetchall()
    return {"buy": buy, "sell": sell}


@app.route('/trade/updateGrid', methods=["get"])
def trade_update_grid():
    '''
        更新网格交易，设置为成交
    :return:
    '''
    warnings.warn("下个版本将要弃用，推荐使用：/trade/pairGrid", DeprecationWarning)
    id = request.args["id"]
    # 使用 cursor() 方法创建一个游标对象 cursor
    connection.ping()
    cursor = connection.cursor(cursor=DictCursor)
    cursor.execute(f"UPDATE trade_line SET grid=0 WHERE id ={id}")
    connection.commit()
    d = cursor.fetchall()
    # print(d)
    return "1"


@app.route('/trade/pairGrid', methods=["get"])
def trade_pair_grid():
    '''
        更新网格交易，设置为成交,成对更新
    :return:
    '''
    id1 = request.args["id1"]
    id2 = request.args["id2"]

    # 使用 cursor() 方法创建一个游标对象 cursor
    connection.ping()
    cursor = connection.cursor(cursor=DictCursor)

    cursor.execute(f"UPDATE trade_line SET grid=0 , pair_id = {id2} WHERE id ={id1}")
    cursor.execute(f"UPDATE trade_line SET grid=0 , pair_id = {id1} WHERE id ={id2}")
    connection.commit()
    d = cursor.fetchall()
    # print(d)
    return "1"


@app.route('/trade/sendEmail', methods=["get"])
def trade_send_email():
    '''
        发送网格交易待成交数据买卖需求邮件
    :return:
    '''

    # 使用 cursor() 方法创建一个游标对象 cursor
    connection.ping()
    cursor = connection.cursor(cursor=DictCursor)
    sql = "SELECT code,type,num,gridPrice FROM trade_line WHERE grid=1"

    # 执行SQL语句
    cursor.execute(sql)
    all_data = {}
    for d in cursor.fetchall():
        print(d)
        code = d["code"]
        if code in all_data:
            grid_data = all_data[code]
        else:
            grid_data = {"sell": [], "buy": []}
            all_data[code] = grid_data
        if d['type'] == "买入":
            grid_data["sell"].append([abs(d["num"]), d["gridPrice"]])
        elif d['type'] == "卖出":
            grid_data["buy"].append([abs(d["num"]), d["gridPrice"]])
    text = ""
    for k in all_data:
        grid_data = all_data[k]
        text += f"股票代码：{k}\n"
        text += "买入\n"
        buy = sorted(grid_data["buy"], key=lambda x: x[1])

        for line in buy:
            text += str(round(line[0], 2)) + "," + str(round(line[1], 2)) + "\n"

        text += "卖出\n"
        sell = sorted(grid_data["sell"], key=lambda x: x[1])
        for line in sell:
            text += str(round(line[0], 2)) + "," + str(round(line[1], 2)) + "\n"
    # print(text)
    send_text("股票推荐", "网格交易", text)
    return "1"


@app.route('/opendays', methods=["get"])
def opendays():
    '''
        查询开盘日期
    :return:
    '''

    start = request.args["start"]
    end = request.args["end"]

    return json.dumps(cds.open_days(start, end))


@app.route('/tradeline', methods=["get"])
def tradeline():
    '''
        查询开盘日期
    :return:
    '''

    startDate = request.args["startDate"]
    currentDate = request.args["currentDate"]

    path = r"E:\File\workspace\python\StockBacktest\data\time_price_000783.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    path2 = r"E:\File\workspace\python\StockBacktest\data/logs/markpoint.json"
    with open(path2, "r", encoding="utf-8") as f:
        markpoint = json.load(f)

    days = cds.open_days(startDate, currentDate)
    allDate = []
    allPrice = []
    allMP = []

    for i in days:
        if i in data.keys():
            for j in data[i]:
                allDate.append(i + " " + j[0])
                allPrice.append(j[1])
            if i in markpoint.keys():
                for mk in markpoint[i]:
                    allMP.append(translate_markpoint(mk))

    singleDate = []
    singlePrice = []
    singleMP = []
    if currentDate in data.keys():
        for j in data[currentDate]:
            singleDate.append(j[0])
            singlePrice.append(j[1])
    if currentDate in markpoint.keys():
        for mk in markpoint[currentDate]:
            singleMP.append(translate_markpoint(mk, use_time=True))

    return {"all": {"DATE": allDate, "PRICE": allPrice, "markpoint": allMP},
            "single": {"DATE": singleDate, "PRICE": singlePrice, "markpoint": singleMP},
            "next": cds.compute_date(currentDate)}


def translate_markpoint(mk, use_time=False):
    """
        将买卖记录转换成echarts的标点
    :param mk: 格式实例：["20220629", "10:19:22", 5.99, 2000, 0]
    :return:
    """
    if use_time:
        x_axis = str(mk[1])
    else:
        x_axis = str(mk[0]) + " " + str(mk[1])

    name = str(mk[2]) + " " + str(mk[3])
    if mk[4] == 0:
        # 买入 但未卖出
        return {
            "coord": [x_axis, mk[2]],
            "value": str(mk[2]),
            "name": name,
            "itemStyle": {
                "color": '#ff0000'
            }
        }
    elif mk[4] == 1:
        # 买入 且 卖出
        return {
            "coord": [x_axis, mk[2]],
            "value": str(mk[2]),
            "name": name,
            "itemStyle": {
                "color": '#8A0000'
            }
        }
    elif mk[4] == 2:
        # 卖出 但未买入
        return {
            "coord": [x_axis, mk[2]],
            "value": str(mk[2]),
            "name": name,
            "itemStyle": {

                "color": '#04fd04'
            }
        }
    elif mk[4] == 3:
        # 卖出 且 买入
        return {
            "coord": [x_axis, mk[2]],
            "value": str(mk[2]),
            "name": name,
            "itemStyle": {
                # ff0000
                "color": '#3c7a3c'
            }
        }
    else:
        return {
            "coord": [x_axis, mk[2]],
            "value": str(mk[2]),
            "name": name,
            "itemStyle": {
                "color": '#00da3c'
            }
        }


@app.route('/update/calendar', methods=["get"])
def calendar():
    '''
        更新交易日历
    :return:
    '''
    end = datetime.datetime.now() + datetime.timedelta(days=30)
    end = end.strftime("%Y%m%d")
    downloader.update_calendar(end_date=end)
    cds.update_date()
    return cds.cal.last_date()


@app.route('/update/codelist', methods=["get"])
def codelist():
    '''
        更新股票列表
    :return:
    '''

    downloader.update_list()
    mapping.load_mapping()

    return json.dumps([i.__dict__ for i in mapping.infos][:100])


@app.route('/update/daily', methods=["get"])
def daily():
    """
        更新股票日线数据
    :return:
    """
    code = request.args["code"]
    code = mapping.get_code(code)
    downloader.update_daily(code)
    cds.load(code)
    result = []
    data = cds.get_code(code)
    for k in data.keys():
        result.append(data[k].__dict__)
    result = sorted(result, key=lambda x: x["trade_date"], reverse=True)
    return json.dumps(result[:100])


@app.route('/update/hs300elements', methods=["get"])
def hs300elements():
    """
        更新沪深300成分股
    :return:
    """
    downloader.update_hs300elements()
    cds.load_hs300elements()

    result = []
    data = cds.hs300_elements
    for k in data.keys():
        result.append(data[k].__dict__)

    return json.dumps(result)


if __name__ == '__main__':
    app.run()
