# -*- coding:utf-8 -*-
# @time:2022/11/1914:48
# @author:LX
# @file:htmlAnalysis.py
# @software:PyCharm
import re
import copy
import random
import requests
import bs4.element
from requests.models import Response
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement


'''

    分析 网站
    输入框: input
    按钮: button,a,div,input
'''

# 抓
class CatchHtml:
    '''
        find_xxx 返回格式
        {
            "se_obj": selenium 元素对象,      # 共有属性
            "bs4_obj":bs4 Tag 对象,          # 共有属性
            "pos": 元素位置,                  # 共有属性
            "attr": 元素属性,                 # 共有属性
            "size": 大小大小,                    # 共有属性
            "value": 值列表,                 # find_select 独有属性
            "text": 文字列表                  # find_select 独有属性
        }


    '''
    def __init__(self,executable_path="chromedriver"):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path=executable_path,options=chromeOptions)
        self.bs4_html = None

    def get(self,url:str):
        self.driver.get(url)
        self.bs4_html = BeautifulSoup(self.driver.page_source, "html.parser")

    def url(self)->str:
        return self.driver.current_url

    @property
    def html(self)->str:
        return self.bs4_html

    # 美化输出
    def prettifyHtml(self):
        print(self.bs4_html.prettify())

    @staticmethod
    def get_coordinates(driver, element):
        '''
            获取元素的位置坐标
        :param element: 元素
        :return:
        '''
        coordinates_mode = 1
        if coordinates_mode == 1:
            # JS代码
            js_code = """var r = arguments[0].getBoundingClientRect();
            return {top: (window.outerHeight - window.innerHeight) + Math.floor(r.top),
            left: Math.floor(r.left), elem_width: r.width, elem_height: r.height}"""
            res = driver.execute_script(js_code, element)
            x = res['left'] + random.randint(int(res['elem_width']) // 3, int(res['elem_width'] * 2 // 3))
            y = res['top'] + random.randint(int(res['elem_height']) // 3, int(res['elem_height'] * 2 // 3))
        elif coordinates_mode == 2:
            win_pos = driver.get_window_position()
            el_size = element.size
            el_xy = element.location
            x = el_xy['x'] + random.randint(int(el_size['width'] // 3), int(el_size['width'] * 2 // 3)) + win_pos[
                'x'] + 8
            y = el_xy['y'] + random.randint(int(el_size['height'] // 3), int(el_size['height'] * 2 // 3)) + win_pos[
                'y'] + driver.execute_script('return window.outerHeight - window.innerHeight;') + 8
        elif coordinates_mode == 3:
            win_pos = driver.get_window_position()
            el_size = element.size
            x = element.location['x'] + random.randint(int(el_size['width'] // 3), int(el_size['width'] * 2 // 3)) + \
                win_pos['x'] + 8
            y = driver.execute_script('return arguments[0].getBoundingClientRect().top', element) + \
                random.randint(int(el_size['height'] // 3), int(el_size['height'] * 2 // 3)) + win_pos[
                    'y'] + driver.execute_script('return window.outerHeight - window.innerHeight;') + 8
        else:
            raise Exception("__get_coordinates__ : without this coordinates mode")
        return x, y

    # 分析属性
    def attribute_analyst(self,label_str:str):
        attr = re.findall(r' (.*?=".*?")', label_str)
        print(attr)

    # 模板
    def __template(self,label_name:str):
        result = []

        # 同步寻找元素
        se_s = self.driver.find_elements("xpath", "//{}".format(label_name))
        bs4_s = self.bs4_html.find_all(label_name)

        # 过滤不可见元素
        show_e_i = [se_s.index(e) for e in se_s if e.is_displayed()]
        se_s = list(filter(lambda e: e.is_displayed(), se_s))
        bs4_s = [bs4_s[i] for i in show_e_i]
        for i in range(len(se_s)):
            temp = dict()

            temp["se_obj"] = se_s[i]
            temp["bs4_obj"] = bs4_s[i]
            temp["pos"] = self.get_coordinates(self.driver, se_s[i])
            temp["attr"] = bs4_s[i].attrs
            temp["size"]  = se_s[i].size

            result.append(temp)
        return result

    def find_input(self):
        return self.__template("input")

    def find_button(self):
        return self.__template("button")

    def find_select(self):
        all_select = self.__template("select")
        for t in all_select:
            t["value"],t["text"] = [],[]
            for i in t["bs4_obj"].children:
                if isinstance(i, bs4.element.Tag):
                    # print(i)
                    t["value"].append(i["value"])
                    t["text"].append(i.text)
        return all_select

    def find_div(self):
        return self.__template("div")

cat =CatchHtml()
# cat.get("https://www.baidu.com/")
cat.get("https://betterhomeupgrade.com/")
# cat.prettifyHtml()

print(cat.find_button())