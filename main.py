#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: hiphp
@license: Apache Licence 
@contact: hi_php@163.com
@site: wuwenfu.cn
@software: PyCharm Community Edition
@file: main.py
@time: 2016/2/2 9:29
"""
import liuanren

def func():
    pass


class Main():
    def __init__(self):
        pass


if __name__ == '__main__':

    liuanren =  liuanren.Liuanren()
    replyinfo = liuanren.get_replyinfo('http://bbs.luanren.com/forum.php?mod=viewthread&tid=5139083&extra=page%3D1')
    liuanren.reply_topic(replyinfo['reply_url'],replyinfo['formhash'],u"小手一抖，经验到手。楼主写的不错。2016新年快乐")
    # liuanren.test()
    pass