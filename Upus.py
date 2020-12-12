# -*- coding:utf-8 -*-


import requests
import xlrd
import sys
from math import ceil
from retrying import retry
from lxml import etree
from Write_csv import Write_csv
from GetProxies import GetProxies


class LOPClass(Write_csv):
    def __init__(self, file_path):
        super().__init__()
        # 按照多少分割
        self.split_num = 35
        # self.file_path = f'./{file_path}.xlsx'
        self.file_path = file_path
        # 访问URL地址
        self.root_url = "https://tools.usps.com/go/TrackConfirmAction"
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
        self.item_list = self.split_item_list(self.read_file())
        # 要保存的csv文件
        self.to_csv = f"{self.file_path}副本"
        # 创建一个csv 文件
        self.create_csv()
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
        pass

    # @retry()
    def get_response(self, params):
        self.headers['Proxy-Authorization'] = self.proxiesClass.get_proxies()
        url = self.root_url + params
        html = requests.get(url=url, headers=self.headers, timeout=10).text
        return html

    def get_data(self):
        for params in self.item_list:
            params = f"?tRef=fullpage&tLc={len(params) + 1}&text28777=&tLabels=" + ",".join(params)
            html = self.get_response(params)
            # print(html)
            self.parse_response(html)

    def parse_response(self, html):
        """
        解析HTML页面
        :return:
        """
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

            self.result_list = [tracking_number, state, sign_time, sign_log, start_time, start_log, two_time, two_log]
            # yield [tracking_number,state, sign_time, sign_log, start_time, start_log, two_time, two_log]
            self.write_excel(self.result_list)


if __name__ == '__main__':
    debug = True

    if debug:
        file_path = "11"
    else:
        file_path = input(f"请输入文件名，和程序同一目录：")
    Lop = LOPClass(file_path)
    Lop.get_data()
