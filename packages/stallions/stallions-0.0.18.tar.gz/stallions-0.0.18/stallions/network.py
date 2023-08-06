import requests
import random
from .config import BROWSER_USER_AGENT

HTTP_DEFAULT_TIMEOUT = 4


class HtmlFetcher(object):
    def __init__(self):
        self.http_timeout = HTTP_DEFAULT_TIMEOUT
        # set header
        self.headers = {'User-agent': random.choice(BROWSER_USER_AGENT), 'Connection': 'close'}

    @staticmethod
    def get_encoding_type(apparent_encoding, html_encoding_list):
        #  utf-8 < GB2312、BIG5、GBK、GB18030
        html_encoding = ''
        if len(html_encoding_list) > 0:
            html_encoding = html_encoding_list[0]
        data_list = [apparent_encoding, html_encoding]
        gbk_list = [x for x in data_list if "GB" in x.upper()]
        if len(gbk_list) > 0:
            return gbk_list[0]
        utf_list = [x for x in data_list if "UTF" in x.upper()]
        if len(utf_list) > 0:
            return utf_list[0]
        return 'UTF-8'

    def get_html(self, url, coding=False):
        # do request
        html = ''
        status = False
        try:
            req = requests.get(url, headers=self.headers, timeout=self.http_timeout)
            header = req.headers
            # 剔除二进制
            content_type = header.get('Content-type', None)
            if content_type == 'application/octet-stream':
                return html, status
            response_encoding_list = requests.utils.get_encodings_from_content(req.text)
            # print(req.headers['content-type'])
            # print("response内容的encoding编码:", req.encoding)
            # print("response headers里设置的apparent_encoding编码:", req.apparent_encoding)
            # print("response返回的html header标签里设置的编码:", response_encoding_list)
            # print(req.status_code)
            if req.status_code >= 400:
                return html, 0
            status = 1
            if coding:
                print(req.encoding, req.apparent_encoding, response_encoding_list)
            if req.encoding == "ISO-8859-1":
                req.encoding = self.get_encoding_type(req.apparent_encoding, response_encoding_list)
            req.keep_alive = False
            # print(html)
            html = req.text
        except Exception as e:
            print(e, "encoding error")
        # print(html, 'html')
        return html, status


class FileFetcher(object):
    @staticmethod
    def get_html(url):
        # do read
        print(url)
        try:
            with open(url, "r", encoding="utf-8") as file_obj:
                html = file_obj.read().strip()
        except Exception as e:
            print(e)
            html = None
        return html
