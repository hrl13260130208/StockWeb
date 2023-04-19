

from exts import db


class TradeLine(db.Model):
    __tablename__ = "trade_line"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(255), comment="日期")
    name = db.Column(db.String(255), comment="股票名称")
    type = db.Column(db.String(255), comment="买卖方向")
    num = db.Column(db.Integer, comment="成交数量")
    price = db.Column(db.Float, comment="成交价格")
    amount = db.Column(db.Float, comment="成交金额")
    code = db.Column(db.String(255), comment="股票代码")
    cost = db.Column(db.Float, comment="手续费")
    tax = db.Column(db.Float, comment="印花税")
    transferCost = db.Column(db.Float, comment="过户费")
    realAmount = db.Column(db.Float, comment="发生金额")
    tradeNum = db.Column(db.String(255), comment="委托号")
    summary = db.Column(db.String(255), comment="摘要")
    grid = db.Column(db.BOOLEAN, comment="是否进行网格交易")
    gridPrice = db.Column(db.Float, comment="网格卖出价格")
    year = db.Column(db.String(255), comment="年份")
    month = db.Column(db.String(255), comment="月份")
    strategy = db.Column(db.Integer, comment="策略")




if __name__ == '__main__':
    db.create_all()






