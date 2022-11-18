# -*- coding:utf-8 -*-
# @time:2022/11/1816:29
# @author:LX
# @file:htmlAnalysis.py
# @software:PyCharm
'''

    分析 网站
'''
import re
import requests
from requests.models import Response

# 抓
class CatchHtml:
    def __init__(self,response:Response=None,encoding="utf-8"):
        response.encoding = encoding
        self.text = response.text

    def setUrl(self,url:str):
        self.url = url

    def body(self):
        return re.findall(r"<body.*</body>",self.text,re.S)[0]

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
}


a=requests.get("https://www.baidu.com/",headers=headers)
cat = CatchHtml(a)
print(cat.body())