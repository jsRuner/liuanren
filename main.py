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
import time
import re
import random

def func():
    pass


class Main():
    def __init__(self):
        pass


if __name__ == '__main__':

    # pattern = re.compile(".*?thread-(.*?)-1-1.html",re.S)
    # result = re.findall(pattern,'http://bbs.luanren.com/thread-5591088-1-1.html')
    # print(result[0])
    # exit()

    liuanren =  liuanren.Liuanren()
    # articles = liuanren.get_newpost()
    # articles = liuanren.get_wenhua()
    articles = liuanren.get_yuer()

    for article in articles:
        # print(article['href'])
        # print(article['title'].decode('gbk'))
        # continue
        # replyinfo = liuanren.get_replyinfo('http://bbs.luanren.com/forum.php?mod=viewthread&tid=5139083&extra=page%3D1')
        print(u"回复文章：%s" % article['href'])
        replyinfo = liuanren.get_replyinfo(article['href'])
        if not replyinfo['status']:
            print(u'该文章未能获取回复的信息：%s' % article['href'])
            continue
        # time.sleep(2)
        msgs = [u"小手一抖，经验到手。楼主写的不错。2016新年快乐",u"这是神一样的十五个字么我的天啊 标准的十五字回复真是越来越多了 我不会告诉你我是专门来混经验的 呦呦！老夫是神话无可超越的神话～呦 看看我的签名貌似真的很黄很暴力 我想肯定会有人数这句话有多少字 如果你真的不知道有这句话的存在 我觉得此帖必删那我先删前留名了",u"现在的小女孩，十几岁毛还没长齐就和人家xxoo了，到二十多岁的时候不知道换了多少男朋友，一个月好几拨。还他妈无耻的大喊男人侮辱了她的身体，骗了她的心。对于这种女人 我只想说四个字:请联系我",u"小手一抖，经验到手。楼主写的不错。2016新年快乐",u"在看完这帖子以后,我没有立即回复,因为我生怕我庸俗不堪的回复会玷污了这网上少有的帖子.但是我还是回复了,因为觉得如果不能在如此精彩的帖子后面留下自己的网名,那我死也不会瞑目的!能够在如此精彩的帖子后面留下自己的网名是多么骄傲的一件事啊!楼主,请原谅我的自私"]

        msgindex = random.randint(0,len(msgs)-1)

        print(msgs[msgindex])
        continue



        liuanren.reply_topic(replyinfo['reply_url'],replyinfo['formhash'],msgs[msgindex])
        time.sleep(6)
    # exit()
    # liuanren.test()
    pass