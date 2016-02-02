#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: hiphp
@license: Apache Licence 
@contact: hi_php@163.com
@site: wuwenfu.cn
@software: PyCharm Community Edition
@file: liuanren.py
@time: 2016/2/2 9:28

saoli
saoli123
"""
import urllib,urllib2,re,json,httplib,time,os,cookielib,urlparse

def func():
    pass


class Liuanren():
    login_url = "http://bbs.luanren.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
    home_url = "http://bbs.luanren.com/"


    # 这里进行登录操作
    def __init__(self):
        self.opener = self.__private_login()

    # 私有方法。登录网站。
    def __private_login(self):
        data={
            "quickforward":"yes",
            "handlekey":"ls",
            "username":"saoli",
            "password":"saoli123"
        }
        #urllib进行编码。
        post_data = urllib.urlencode(data)
        #初始化一个CookieJar来处理Cookie。
        ckjar = cookielib.MozillaCookieJar('c:\\liuanren.txt')
        ckproc = urllib2.HTTPCookieProcessor(ckjar)
        # 实例化一个全局opener。
        opener=urllib2.build_opener(ckproc)
        # 获取cookie。
        req = urllib2.Request(Liuanren.login_url,post_data)
        opener.open(req)
        # 保存cookie
        ckjar.save(ignore_discard=True, ignore_expires=True)
        return opener;
    # http://bbs.luanren.com/forum.php?mod=post&action=reply&fid=3&tid=5591403&extra=page%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1
    def reply_topic(self,reply_url,formhash,msg):
        # 获取表单formhash
        headers = {
           # "Referer": "http://bbs.168hs.com/forum.php?mod=post&action=newthread&fid=159",
            "Host": "bbs.luanren.com",
        }
        data={
            "formhash":formhash,
            "posttime":time.time(),
            "message":msg.encode('gbk')
        }
        #urllib进行编码。
        post_data = urllib.urlencode(data)
        req3 = urllib2.Request(reply_url,post_data,headers)
        rs = self.opener.open(req3)
        print(rs.read().decode('gbk'))
        pass
        # 提交回复。
    # 获取回复帖子需要的地址与表达formhash.
    # 先取帖子的地址。解析出tid参数即可。
    #
    def get_replyinfo(self,topic_url):
        xx = self.opener.open(urllib2.Request(topic_url))
        topic_html = xx.read()
        pattern = re.compile('<input type="hidden" name="formhash" value="(.*?)" />',re.S)
        formhashs = re.findall(pattern,topic_html)

        formhash = ""
        if formhashs:
            for item in formhashs:
                formhash = item
                print(item)# 901ec69e

        if formhash == "":
            print(u"获取表单formhash失败")
            exit()

        # 解析参数
        result=urlparse.urlparse(topic_url)
        urlparse.parse_qs(result.query,True)
        params=urlparse.parse_qs(result.query,True)
        reply_url = "http://bbs.luanren.com/forum.php?mod=post&action=reply&fid=3&tid="+params['tid'][0]+"&extra=page\%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1"
        return {"formhash":formhash,"reply_url":reply_url}

    def test(self):
        req2 = urllib2.Request(Liuanren.home_url)
        result2 = self.opener.open(req2)
        print(result2.read().decode('gbk'))





if __name__ == '__main__':
    pass