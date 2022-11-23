# -*- coding:utf-8 -*-
# @time:2022/11/2217:58
# @author:LX
# @file:controlsAttr.py
# @software:PyCharm


# 控件类型
class ControlsType:
    Input = "input"
    Div = "div"
    A = "a"
    Button = "button"
    Select = "select"


# 控件样式
class ControlsStyle:
    CStyle = {
        "input":'''
border:1px solid rgb(131, 131, 0);
background-color:transparent;
        ''',
        "div":'''
border:2px dotted rgb(225, 112, 169);
        ''',
        "a":'''
border:1px solid rgb(5, 134, 255);
border-top:none;
border-left:none;
border-right:none;
background-color:transparent;
        ''',
        "button":'''
border:1px solid rgb(85, 170, 0);
background-color:transparent;
        ''',
        "select":'''
border:1px solid rgb(85, 170, 0);
background-color:transparent;
        '''
    }