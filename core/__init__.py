# -*- coding:utf-8 -*-
# @time:2022/11/1816:28
# @author:LX
# @file:__init__.py.py
# @software:PyCharm
'''

    执行流程

    扫描网站 -> 网站结构解体(headr body scrpit) -> 多线程分析Body() -> 分析页面的执行流程
    -> 寻找按钮
    -> 寻找输入框                                                  -> 成功  保留结果
    -> 寻找标题                 -> 生成 xpath     ->   验证xpath
    -> 寻找下拉框(select,div)                                      -> 失败  结果待定  --> 继续进入多线程分析
    -> 选择多选框

                             |
                             |
                        全部分析完成生成自动化代码
                             |
                           检测
'''