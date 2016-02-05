#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: hiphp
@license: Apache Licence 
@contact: hi_php@163.com
@site: wuwenfu.cn
@software: PyCharm Community Edition
@file: RobFloors.py
@time: 2016/2/5 13:10
"""
import threading
import time
import urlparse
import re
import urllib,urllib2,os,json
class MyThread(threading.Thread):
    """
    属性:
    target: 传入外部函数, 用户线程调用
    args: 函数参数
    """
    def __init__(self, target, args):
        super(MyThread, self).__init__()  #调用父类的构造函数
        self.target = target
        self.args = args

    def run(self) :
        self.target(self.args)

# 获取指定楼层的账号。参数有 帖子链接，楼层的数字。
# http://bbs.luanren.com/thread-4139087-1-1.html 要求帖子url格式如此。或者是?这样的
#http://bbs.luanren.com/forum.php?mod=viewthread&tid=4139087
#指定楼层的url 转换。http://bbs.luanren.com/forum.php?mod=redirect&ptid=4139087&authorid=0&postno=200
# 正则匹配该楼层的账号。
def get_username(topic_url,num):
    username = False
    result = urlparse.urlparse(topic_url)
    tid = False #初始赋值。
    if result.query == "": #url没有携带参数的
        pattern = re.compile(".*?thread-(.*?)-\d-\d.html", re.S)
        result = re.findall(pattern, topic_url)
        if result:
            tid = result[0]
    else: #携带了?
        urlparse.parse_qs(result.query, True)
        params = urlparse.parse_qs(result.query, True)
        tid = params['tid'][0]
    if not tid:
        print(u"未获取tid。文章url不符合要求。")
        exit()
    floor_url = "http://bbs.luanren.com/forum.php?mod=redirect&ptid=%s&authorid=0&postno=%d" % (tid,num)
    print(u"当前网址: %s" %floor_url)
    #访问楼层url
    html = urllib.urlopen(floor_url).read()
    pattern = re.compile('<td class="pls" rowspan="2">.*?<strong><a.*?>(.*?)</a></strong>.*?</td>.*?<td class="plc">.*?<em>(.*?)</em>.*?</td>',re.S)
    result = re.findall(pattern,html)
    if result:
        for item in result:
            if item[1] == '200':
                username = item[0]
                print(u"当前楼层的用户名:" % item[0])
    return username
# 获取当前帖子最后楼层的编号。参数:帖子的url
# 获取分页。访问最后一页。
def get_lastnum(topic_url):
    page = 1
    html = urllib.urlopen(topic_url).read()
    pattern1 = re.compile('<label>.*?<span title="(.*?)"> /.*?</span>.*?</label>',re.S)
    result1 = re.findall(pattern1,html)
    if result1:
        for item in result1:
            # print(item)
            page = filter(str.isalnum,item)
            break #匹配到一个就结束了。
    print("匹配的页数为 %s" % page)

    # 获取tid。要求url必须有规则。符合要求。
    result = urlparse.urlparse(topic_url)
    tid = False #初始赋值。
    if result.query == "": #url没有携带参数的
        pattern = re.compile(".*?thread-(.*?)-\d-\d.html", re.S)
        result = re.findall(pattern, topic_url)
        if result:
            tid = result[0]
    else: #携带了?
        urlparse.parse_qs(result.query, True)
        params = urlparse.parse_qs(result.query, True)
        tid = params['tid'][0]
    if not tid:
        print(u"未获取tid。文章url不符合要求。")
        exit()

    # 最后一页的url
    last_url = "http://bbs.luanren.com/thread-%s-%s-1.html" % (tid,page)
    print(last_url)
    num = 1 #最后楼层为1.默认的值。
    html2 = urllib.urlopen(last_url).read()
    pattern2 = re.compile('<td class="pls" rowspan="2">.*?<strong><a.*?>(.*?)</a></strong>.*?</td>.*?<td class="plc">.*?<em>(.*?)</em>.*?</td>',re.S)
    result2 = re.findall(pattern2,html2)
    if result2:
        lastfloor= result2[-1]
        num = lastfloor[1]
    print("当前帖子最后的楼层数为 %s" % num)
    return num
# 获取配置文件信息。
def get_config():
    pass

# 修改配置文件的信息。配置信息。todo：多个账号咋办。
def set_config():
    pass

# 回复帖子。



# 抢楼的线程执行的函数。需要传递特定的账号。回复的信息。进行抢楼操作。

#判断是否中奖的函数。中了则修改配置文件。没中则不操作。 决定账号是否还继续进行回复的操作

#判断当前的楼层。靠近则修改配置文件。超过了则修改配置文件。 控制回帖的速度。








# 主程序
def main():
    # get_username("http://bbs.luanren.com/forum.php?mod=viewthread&tid=4139087",200)
    # get_username("http://bbs.luanren.com/forum.php?mod=viewthread&tid=4139087&page=1#pid5107373",200)
    # get_lastnum("http://bbs.luanren.com/forum.php?mod=viewthread&tid=4139087")
    get_lastnum("http://bbs.luanren.com/thread-5591889-1-1.html")
    pass


if __name__ == '__main__':
    main()