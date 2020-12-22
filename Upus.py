# -*- coding:utf-8 -*-
import time
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import re
from threading import Thread
from queue import Queue
import PyQt5.sip
import requests
import xlrd
import calendar
import sys
from math import ceil
from retrying import retry
from lxml import etree
from Write_csv import Write_csv
from GetProxies import GetProxies


class LOPClass(QtCore.QThread):
    # 定义信号参数为list
    update_data = QtCore.pyqtSignal(str)
    stop_singin = QtCore.pyqtSignal(bool)

    def __init__(self, file_path, sleep_time, thread_num, is_proxies):
        super().__init__()
        # 按照多少分割
        self.split_num = 35
        # self.file_path = f'./{file_path}.xlsx'
        self.file_path = file_path
        self.sleep_time = int(sleep_time)
        self.thread_num = int(thread_num)
        self.is_proxies = is_proxies
        # 线程队列
        self.params_queue = Queue()
        self.number = 0
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
        # 列表开始去重
        item_list = list(set(item_list))
        self.update_data.emit(f"参数已经作去重处理，共有参数：{len(item_list)}个")
        new_item_list = []
        num = 0
        for i in range(ceil(len(item_list) / self.split_num)):
            if item_list[num:num + self.split_num]:
                new_item_list.append(item_list[num:num + self.split_num])
                num += self.split_num
        return new_item_list

    def queue_put(self):
        for params in self.item_list:
            self.params_queue.put(params)

        if self.thread_num > 1:
            self.update_data.emit(f"多线程队列写入成功，共有线程{self.thread_num}个")

    def run(self):
        self.queue_put()
        self.update_data.emit("-------------开始查询，请勿多次点击！-------------")
        print("开始了！")
        thread_list = []
        for i in range(self.thread_num):
            t = Thread(target=self.start_thread)
            t.setDaemon(True)
            t.start()
            thread_list.append(t)
        for t in thread_list:
            t.join()

        self.update_data.emit("-------------查询结束了-------------")
        self.stop_singin.emit(True)

    def start_thread(self):
        while not self.params_queue.empty():
            params = self.params_queue.get()
            self.get_data(params)

    @retry(stop_max_attempt_number=5, wait_random_min=1000, wait_random_max=3000)
    def get_response(self, params):
        url = self.root_url + params
        # true 代表使用代理
        if self.is_proxies:
            # 初始化IP
            proxiesClass = GetProxies()
            self.headers['Proxy-Authorization'] = proxiesClass.get_proxies()
            html = requests.get(url=url, headers=self.headers, proxies=proxiesClass.proxies, verify=False,
                                timeout=10).text
        else:
            html = requests.get(url=url, headers=self.headers, verify=False, timeout=10).text
        return html

    def get_data(self, param):
        params = f"?tRef=fullpage&tLc={len(param) + 1}&text28777=&tLabels=" + ",".join(param)
        try:
            # self.update_data.emit(f"当前携带参数个数共 {len(param)}  个")
            html = self.get_response(params)
        except Exception as e:
            print(e)
            self.update_data.emit("程序出现以下错误：只是简单的代理IP失效了而已！")
            self.update_data.emit(str(e))
            self.params_queue.put(param)
            self.update_data.emit("参数已经重新上传，请耐心等待。")
            html = None
        time.sleep(int(self.sleep_time))
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
            print(start_time)
            print(f"结束时间：{two_time}")
            start_time = self.formatting_time(start_time)
            two_time = self.formatting_time(two_time)
            # global result_list
            # self.result_list = [tracking_number, state, sign_time, sign_log, start_time, start_log, two_time, two_log]
            # self.csv.write_excel(self.result_list)
            self.number += 1
            result_list = ["'" + tracking_number, state, sign_time, sign_log, start_time, start_log, two_time, two_log]
            self.csv.write_excel(result_list)
            result_list.append(f"当前存入共{self.number}个")
            self.update_data.emit(",".join(result_list))

    @staticmethod
    def formatting_time(format_time):
        """
        输入一个没有格式化的时间，开始格式化     # November 24, 2020, 下午 11:56
        :param format_time:  未格式化时间
        :return: 格式化之后的  2020年 11月24号，下午11:56
        """
        month = re.match("\S+", format_time)
        day = re.search("\d+", format_time)
        year = re.search("\d{4}", format_time)
        hour_minute_second = re.search("[\u4e00-\u9fa5]{1,2} \d{1,2}:\d{1,2}", format_time)

        month = month.group() if month else ""
        month = list(calendar.month_name).index(month)
        day = day.group() if day else ""
        year = year.group() if year else ""
        hour_minute_second = hour_minute_second.group() if hour_minute_second else ""
        return f"{year}年{month}月{day}日 {hour_minute_second}"


if __name__ == '__main__':
    aa = LOPClass.formatting_time("November 29, 2020")
    print(aa)
