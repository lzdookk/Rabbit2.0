import argparse
import datetime
import json
import re

import pytz
from bs4 import BeautifulSoup

import ustclogin

ORIGIN = "https://weixine.ustc.edu.cn/2020"
SERVICE = "https://weixine.ustc.edu.cn/2020/caslogin"
EXAM = "https://weixine.ustc.edu.cn/2020/home"
REPORT_URL = "http://weixine.ustc.edu.cn/2020/daliy_report"
DATE_PATTERN = re.compile(r"202\d-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}")


def text2soup(text: str):
    markup = text.encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return BeautifulSoup(markup, 'html.parser')


class Report(object):
    def __init__(self, stuid, password, data_path) -> None:
        self.stuid = stuid
        self.password = password
        self.data_path = data_path

    def report(self) -> bool:
        session = ustclogin.Session(self.stuid, self.password, ORIGIN, SERVICE, EXAM)
        success, result = session.login()

        if not success:
            # 登陆失败
            return False

        soup = text2soup(result.text)
        token = soup.find("input", {"name": "_token"})['value']

        with open(self.data_path, "r+") as f:
            data = f.read()
            data = json.loads(data)
            data["_token"] = token

        headers = {
            "content-type": "application/x-www-form-urlencoded",
        }

        # 上报数据
        session.post(REPORT_URL, data=data, headers=headers)

        # 获取最近一次打卡时间
        result = session.get("http://weixine.ustc.edu.cn/2020")
        soup = text2soup(result.text)
        token = soup.find("span", {"style": "position: relative; top: 5px; color: #666;"})
        if DATE_PATTERN.search(token.text) is not None:
            date = DATE_PATTERN.search(token.text).group()
            print("Latest report: " + date)
            date = date + " +0800"
            reporttime = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S %z")
            timenow = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
            delta = timenow - reporttime
            print("{} second(s) before.".format(delta.seconds))
            # 上一次打卡时间距现在小于120s则打卡成功
            if delta.seconds < 120:
                print("Report successful!")
                return True
        print("Report failed!")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='URC nCov auto report script.')
    parser.add_argument('data_path', help='path to your own data used for post method', type=str)
    parser.add_argument('stuid', help='your student number', type=str)
    parser.add_argument('password', help='your CAS password', type=str)
    args = parser.parse_args()
    autorepoter = Report(stuid=args.stuid, password=args.password, data_path=args.data_path)

    # 打卡结果
    if autorepoter.report():
        exit(0)
    else:
        exit(-1)
