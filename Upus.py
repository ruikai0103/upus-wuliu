# -*- coding:utf-8 -*-
import time
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import re
from threading import Thread
import PyQt5.sip
import requests
import xlrd
import sys
from math import ceil
from retrying import retry
from lxml import etree
from Write_csv import Write_csv
from GetProxies import GetProxies


class LOPClass(QtCore.QThread):
    # 定义信号参数为list
    update_data = QtCore.pyqtSignal(str)

    def __init__(self, file_path, sleep_time, thread_num):
        super().__init__()
        # 按照多少分割
        self.split_num = 35
        # self.file_path = f'./{file_path}.xlsx'
        self.file_path = file_path
        self.sleep_time = sleep_time
        self.thread_num = thread_num
        # 访问URL地址
        self.root_url = "https://zh-tools.usps.com/go/TrackConfirmAction"
        self.headers = {
            'authority': 'tools.usps.com',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://tools.usps.com/go/TrackConfirmAction?tRef=fullpage^&tLc=7^&text28777=^&tLabels=420802239374869903505842406011^%^2C420902329374869903505842405182^%^2C420562659374869903505842403935^%^2C420211229374869903505842405106^%^2C420704499374869903505842405069^%^2C420930369374869903505842404963^%^2C',
            'accept-language': 'zh-CN,zh;q=0.9',
        }
        self.csv = Write_csv()
        self.item_list = self.split_item_list(self.read_file())
        # 要保存的csv文件
        self.csv.to_csv = f"{self.file_path.replace('.xlsx', '副本.csv')}"
        # 创建一个csv 文件
        self.csv.create_csv()
        self.update_data.emit("副本文件创建成功！")
        self.proxiesClass = GetProxies()

    def read_file(self):
        """
        获取文件，打开文件 返回列表
        :param filename:
        :return:
        """
        try:
            data = xlrd.open_workbook(self.file_path)
        except FileNotFoundError:
            print(f'文件不存在，程序3秒后退出')
            sys.exit()
        # 查看工作表
        data.sheet_names()
        table = data.sheet_by_name(data.sheet_names()[0])
        sum_list = table.col_values(0)
        sum_list = [i for i in sum_list if i != '']
        return sum_list

    def split_item_list(self, item_list):
        """
        按照item_list分割成一个新的list
        :param item_list:
        :return:
        """
        new_item_list = []
        num = 0
        for i in range(ceil(len(item_list) / self.split_num)):
            if item_list[num:num + self.split_num]:
                new_item_list.append(item_list[num:num + self.split_num])
                num += self.split_num
        return new_item_list

    def run(self):
        self.update_data.emit("-------------开始查询，请勿多次点击！-------------")
        print("开始了！")
        self.get_data(self.sleep_time)
        self.update_data.emit("-------------查询结束了-------------")

    @retry(stop_max_attempt_number=5, wait_random_min=1000, wait_random_max=3)
    def get_response(self, params):
        self.headers['Proxy-Authorization'] = self.proxiesClass.get_proxies()
        url = self.root_url + params
        # self.update_data.emit(f"开始请求的URL为：{url}")
        # self.update_data.emit(f"当前参数为：{params}")
        html = requests.get(url=url, headers=self.headers, proxies=self.proxiesClass.proxies, verify=False,
                            timeout=10).text
        return html

    def get_data(self, sleep_time=0):
        for param in self.item_list:
            params = f"?tRef=fullpage&tLc={len(param) + 1}&text28777=&tLabels=" + ",".join(params)
            try:
                self.update_data.emit(f"当前携带参数个数共 {len(param)}  个")
                html = self.get_response(params)
            except Exception as e:
                print(e)
                self.update_data.emit("程序出现以下错误：请联系开发人员")
                self.update_data.emit(str(e))
                html = None
            time.sleep(int(sleep_time))
            self.parse_response(html)

    def parse_response(self, html):
        """
        解析HTML页面
        :return:
        """
        if not html:
            return
        html = etree.HTML(html)
        for i in html.xpath("//div[contains(@class,'col-sm-offset-1')]"):
            # 获取单号
            tracking_number = i.xpath('normalize-space(.//span[@class="tracking-number"]/text())')
            # 获取状态
            state = i.xpath('normalize-space(.//div[@class="delivery_status"]/h2/strong/text())')
            sign_time = i.xpath('normalize-space(.//div[@class="status_feed"]/p[1]/text())')
            sign_log = i.xpath('normalize-space(.//div[@class="status_feed"]/p[last()]/text())')

            # 第一个物流和第一个物流的时间
            start_log = i.xpath(
                'normalize-space(.//div[@class="panel-actions-content thPanalAction"]/span[last()-1]/text())')
            start_time = i.xpath(
                'normalize-space(.//div[@class="panel-actions-content thPanalAction"]/hr[last()-1]/following-sibling::span[1]/strong/text())')
            # 获取第二个物流和时间
            two_log = i.xpath(
                'normalize-space(.//div[@class="panel-actions-content thPanalAction"]/hr[last()-2]/following-sibling::span[3]/text())')
            two_time = i.xpath(
                'normalize-space(.//div[@class="panel-actions-content thPanalAction"]/hr[last()-2]/following-sibling::span[1]/strong/text())')

            # global result_list
            # self.result_list = [tracking_number, state, sign_time, sign_log, start_time, start_log, two_time, two_log]
            # self.csv.write_excel(self.result_list)
            result_list = [tracking_number, state, sign_time, sign_log, start_time, start_log, two_time, two_log]
            self.csv.write_excel(result_list)
            self.update_data.emit(",".join(result_list))


if __name__ == '__main__':
    debug = True

    if debug:
        file_path = "11"
    else:
        file_path = input(f"请输入文件名，和程序同一目录：")
    Lop = LOPClass(file_path)
    Lop.get_data(1)
