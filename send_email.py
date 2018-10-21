import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import mimetypes

# 第三方 SMTP 服务
mail_host = "smtp.163.com"   # SMTP服务器
mail_user = 'xxxxxxx'    # 用户名
mail_pass = 'xxxxxxxx'     # 密码

sender = 'xxxxx@163.com'    # 发件人邮箱

title = 'NBA数据分析任务定时发送'  # 邮件主题


def save_data_to_excel_csv(python_data, file_name='NBAdata.csv', ):
    with open(file_name, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='excel')
        csvwriter.writerows(python_data)


def generate_email_file_and_data(team_data, all_team=False, team_name=None):
    ll = [('球队', '得分第一', '篮板第一', '抢断第一')]
    if not all_team:
        t_data = (team_name,)
        for k, v in team_data.items():
            t_data += (v, )
        ll.append(t_data)
    if all_team:
        for team_name, data in team_data.items():
            t_data = (team_name, )
            for k, v in data.items():
                t_data += (v,)
            ll.append(t_data)

    save_data_to_excel_csv(ll)
    return ll


def send_email(receivers, file_path='NBAdata.csv'):
    message = MIMEMultipart()
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    ctype, encoding = mimetypes.guess_type(file_path)
    if not ctype or encoding:
       ctype = "application/octet-stream"
    # ret = generate_email_file_and_data(team_data, all_team=False, team_name=team_name)

    maintype, subtype = ctype.split("/", 1)

    with open(file_path, "rb") as fp:
        file_content = fp.read()

    attachment = MIMEBase(maintype, subtype)
    attachment.set_payload(file_content)

    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=file_path)
    message.attach(attachment)
    message.attach(MIMEText(file_content, 'plain', 'utf-8'))

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)

