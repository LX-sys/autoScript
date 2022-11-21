# -*- coding:utf-8 -*-
# @time:2022/11/1816:30
# @author:LX
# @file:writeCode.py
# @software:PyCharm
'''

    自动编自动化代码
'''
import re
import sys

class WriteCode:
    def __init__(self):
        pass

    # 分析 label字符串,并返回xpath
    def labelAnalysis(self,label_str:str):
        label_name = label_str.split(" ")[0].replace("<", "")
        attr = re.findall(r' (.*?=".*?")', label_str)
        attr_dict = dict()
        for a in attr:
            k,v = a.split("=")
            attr_dict[k]=v

        if "id" in attr_dict:
            print("//{}[@id={}]".format(label_name,attr_dict["id"]))
            return "//{}[@id={}]".format(label_name,attr_dict["id"])

        if "type" in attr_dict and "class" in attr_dict:
            print("//{}[@type={} and @class={}]".format(label_name,attr_dict["type"],attr_dict["class"]))
            return "//{}[@type={} and @class={}]".format(label_name,attr_dict["type"],attr_dict["class"])

    # 生成代码
    def wCode(self,xpath):
        '''

            这里展示先写死,后面改为模板
        :param xpath:
        :return:
        '''
        if "input" in xpath:
            return "am.send(am.see(\'xpath\',\'{}\')[0],'xxx')".format(xpath)

        if "button" in xpath:
            return "am.click(am.see(\'xpath\',\'{}\')[0])".format(xpath)

        if "select" in xpath:
            return "am.select(am.see(\'xpath\',\'{}\')[0],random.randint(1,10))".format(xpath)