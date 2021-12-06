import re
from typing import Tuple

import requests


class Session(requests.Session):
    def __init__(self, stuid: str, password: str, origin: str, service: str, exam: str) -> None:
        self.stuid = stuid
        self.password = password
        self.origin = origin
        self.service = service
        self.exam = exam
        super().__init__()

    def __passport(self) -> None:
        result = self.get('https://passport.ustc.edu.cn/login?service=' + self.service)
        (cas_lt,) = re.findall(r"name=\"CAS_LT\" value=\"(.+)\"", result.text)
        # 获取登陆验证码, 这一行不能删除, 必须要获取验证码才可以登陆(即使后面可以绕过验证码)
        self.get('https://passport.ustc.edu.cn/validatecode.jsp?type=login', stream=True)
        # showCode = '0' 绕过验证码
        data = {
            'model': 'uplogin.jsp',
            'service': self.service,
            'warn': '',
            'showCode': '0',
            'username': self.stuid,
            'password': self.password,
            'button': '',
            'CAS_LT': cas_lt,
            'LT': ''
        }
        self.post('https://passport.ustc.edu.cn/login', data=data)

    def login(self, retrycount: int = 5) -> Tuple[bool, requests.Response]:
        """
        登陆USTC
        """
        success = False
        while (not success) and retrycount:
            self.__passport()
            result = self.get(self.origin)
            retrycount = retrycount - 1
            if result.url != self.exam:
                print("Login failed! Retry...")
            else:
                print("Login successful!")
                success = True
        return success, result
