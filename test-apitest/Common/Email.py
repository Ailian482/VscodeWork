import os
import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Config import ReadConfig


class send_email:
    '''
    发送邮件功能
    '''

    def __init__(self):
        self.readconfig = ReadConfig.readconfig()
        self.dirpath = self.readconfig.get_basepath("base_path")
        self.report_path = os.path.join(self.dirpath, 'Report')

    #  将表格的路径存入列表
    def make_attachment(self):
        filePathList = []
        tablePath = os.path.join(self.dirpath, 'TestFile')
        for file in os.listdir(tablePath):
            if str(file).endswith(".xls"):
                filePathList.append(os.path.join(tablePath, file))
        return filePathList

    def send_mail(self, user_list, sub, content):
        user = self.readconfig.getEmail("send_user")
        message = MIMEMultipart()
        message['Subject'] = sub
        message['From'] = user  # 发件人
        message['To'] = user_list  # 收件人

        message.attach(MIMEText(content, 'html', 'utf-8'))

        # 构造附件1，传送TestFile目录下的 .xls文件

        fileList = self.make_attachment()
        if fileList:
            for file in fileList:
                filename = os.path.basename(file)
                att1 = MIMEText(open(file, 'rb').read(), 'base64', 'utf-8')
                att1["Content-Type"] = 'application/octet-stream'
                # 邮件中显示的附件名字
                att1["Content-Disposition"] = 'attachment; filename={0}'.format(filename)
                message.attach(att1)

        # 构造附件2，传送当前目录下的 report.html 文件
        # 获取最新文件
        file_lists = os.listdir(self.report_path)
        file_lists.sort(key=lambda fn: os.path.getmtime(self.report_path + "//" + fn)
        if not os.path.isdir(self.report_path + "//" + fn) else 0)
        path = os.path.join(self.dirpath, 'Report', file_lists[-1])  # 获取最新文件
        att2 = MIMEText(open(path, 'rb').read(), 'base64', 'utf-8')
        att2["Content-Type"] = 'application/octet-stream'
        att2.add_header('Content-Disposition', 'attachment',
                        filename=file_lists[-1])
        message.attach(att2)
        try:
            server = smtplib.SMTP()
            # server = smtplib.SMTP_SSL()
            # server.set_debuglevel(1)   #打印发送邮箱日志
            server.connect(self.readconfig.getEmail("email_host"), port=25)
            server.login(self.readconfig.getEmail("send_user"), self.readconfig.getEmail("password"))
            server.sendmail(user, user_list.split(','), message.as_string())
            server.quit()
            print("send email to '{0}' success!".format(user_list))
            return "发送邮件成功"
        except smtplib.SMTPException as e:
            print('无法发送邮件:{0}'.format(e))
            return "发送邮件失败"
        except socket.gaierror as e:
            print('邮件socket错误:{0}'.format(e))

    def find_new_file(self):

        '''查找目录下最新的文件'''
        file_lists = os.listdir(self.report_path)

        file_lists.sort(key=lambda fn: os.path.getmtime(self.report_path  + "\\" + fn)
        if not os.path.isdir(self.report_path  + "\\" + fn) else 0)
        # file = os.path.join(self.report_path , file_lists[-1])  #/全路径
        return file_lists[-1]

if __name__ == '__main__':

    # user_list="'zhengwenpei@tehang.com','hoze163@163.com'"
    user_list="zhengwenpei@tehang.com"
    # user_list="hoze163@163.com"
    # ['john.doe@example.com', 'john.smith@example.co.uk']
    #554发送失败——解决方法：收件人加上发件人本身
    # file = send_email().find_new_file()
    # print(file)
    sen = send_email().send_mail(user_list, u'自动化测试报告','测试发送')
    print(sen)
