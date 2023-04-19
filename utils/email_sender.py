import logging
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime

logger = logging.getLogger("email_sender")
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "2046391563@qq.com"  # 用户名
mail_pass = "eaxudscysqpnegcf"  # 口令

sender = '2046391563@qq.com'
receivers = ['2046391563@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱


def send_recommend(date,buy_codes,sell_codes):
    # 第三方 SMTP 服务
    text = generate_signal_text(date, buy_codes, sell_codes)
    subject = f'股票推荐-{date}'
    send(text,subject)



def send(text,subject):
   header = "股票推荐"
   send_text(header,subject,text)

def send_text(header,subject,text):
    logger.info("发送邮件...")
    message = MIMEText(text, 'plain', 'utf-8')
    message['From'] = sender
    message['To'] = Header(header, 'utf-8')

    message['Subject'] = Header(subject, 'utf-8')

    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 587)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())


def generate_signal_text(date,buy_codes,sell_codes):

    text = f'运行时间：{date}。\n \n买入股票如下：\n'

    for c in buy_codes:
        text+=f"股票代码：{c[0]},买入数量：{c[1]},推荐原因：{c[2]} \n"

    text += f'\n卖出股票如下：\n'
    for c in sell_codes:
        text+=f"股票代码：{c[0]},卖出数量：{c[1]},卖出原因：{c[2]} \n"

    return text





if __name__ == '__main__':
    # generate_signal_text()
    text="aaaaaaaaaaa"
    send_text("股票推荐", "网格交易", text)

