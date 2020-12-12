# -*- coding:utf-8 -*-
import time
import hashlib
import urllib3


class GetProxies:
    def __init__(self):
        self.ip = "forward.xdaili.cn"
        self.prot = 80
        self.proxies = {"http": f"http://{self.ip}:{self.prot}", "https": f"https://{self.ip}:{self.prot}"}
        self.orderno = "ZF20205202306YCxov6"
        self.secret = "0c6e58691e9b4558b6004f14627ecc8f"

    def get_proxies(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # ip = "forward.xdaili.cn"
        # port = "80"

        # ip_port = ip + ":" + port

        timestamp = str(int(time.time()))
        string = "orderno=" + self.orderno + "," + "secret=" + self.secret + "," + "timestamp=" + timestamp

        string = string.encode()

        md5_string = hashlib.md5(string).hexdigest()
        sign = md5_string.upper()
        # print(sign)
        auth = "sign=" + sign + "&" + "orderno=" + self.orderno + "&" + "timestamp=" + timestamp
        return auth

if __name__ == '__main__':
    proxies = GetProxies()
    auto = proxies.get_proxies()
    print(auto)