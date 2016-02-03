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
    # 还需要fid http://bbs.luanren.com/forum.php?mod=forumdisplay&fid=238
    #
    def get_replyinfo(self,topic_url):
        xx = self.opener.open(urllib2.Request(topic_url))
        status = True #状态。true表示可以回复
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
            status = False
            return {"status":status}
            # exit()

        # 解析参数.判断url是否存在tid。如果不存在，则执行正则
        result=urlparse.urlparse(topic_url)
        if result.query == "":
            pattern = re.compile(".*?thread-(.*?)-\d-\d.html",re.S)
            result = re.findall(pattern,topic_url)
            if result:
                tid = result[0]
            else:
                print(u'获取tid失败')
                status = False
                return {"status":status}
                # exit()

        else:
            urlparse.parse_qs(result.query,True)
            params=urlparse.parse_qs(result.query,True)
            tid = params['tid'][0]
        if not tid.isdigit():
            print(u"获取文章的tid失败")
            status = False
            return {"status":status}
            # exit()

        # 获取fid <a href="http://bbs.luanren.com/forum.php?mod=forumdisplay&amp;fid=238">返回列表</a>
        fid_url = ''
        fid = ''
        pattern2 = re.compile('<span class="pgb y"><a href="(.*?)">.*?</a></span>',re.S)
        result2 = re.findall(pattern2,topic_html)
        if result2:
            fid_url = result2[0]
            # print(fid)
            # exit()
        if fid_url == '':
            print(u"获取fid_url失败")
            status = False
            return {"status":status}
            # exit()
        else:
            # 解析fid
            result3=urlparse.urlparse(fid_url)
            if result3.query == "":
                print(u"fid_url没有包含fid参数")
                status = False
                return {"status":status}
                # exit()
            else:
                params3=urlparse.parse_qs(result3.query,True)
                fid = params3['fid'][0]
        print(fid)
        # exit()

        reply_url = "http://bbs.luanren.com/forum.php?mod=post&action=reply&fid="+fid+"&tid="+tid+"&extra=page\%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1"
        return {"formhash":formhash,"reply_url":reply_url,"status":status}
    # 获取最新发布的帖子。包含链接。时间 作者。
    def get_newpost(self):
        html = urllib.urlopen("http://bbs.luanren.com/forum.php?mod=guide&view=newthread").read()
        # print(html.decode('gbk'))
        # <a href="http://bbs.luanren.com/forum.php?mod=viewthread&amp;tid=5591445&amp;extra=" target="_blank" class="xst">男人常吃豆腐 精子“减产”</a>
        pattern_article = re.compile('<th class="common">.*?<a href="(.*?)" target="_blank".*?>(.*?)</a>.*?</th>',re.S);
        result_article = re.findall(pattern_article,html)
        #帖子列表。里面每一个元素是一个帖子。一个帖子是一个字典。
        articles = []
        if result_article:
            for item in result_article:
                # print item
                # exit()
                # continue
                #每一个帖子都是一个字典。包含2个key
                article = {}
                article['href'] = item[0]
                article['title'] = item[1]
                #print article
                # print item[1].decode('gbk')
                # continue
                #添加帖子到列表尾部
                articles.append(article)
        return articles
    def get_wenhua(self):
        html = urllib.urlopen("http://bbs.luanren.com/forum.php?mod=forumdisplay&fid=220").read()
        # print(html.decode('gbk'))
        # <a href="http://bbs.luanren.com/forum.php?mod=viewthread&amp;tid=5591445&amp;extra=" target="_blank" class="xst">男人常吃豆腐 精子“减产”</a>
        pattern_article = re.compile('<a href="http://bbs.luanren.com/thread(.*?)".*?onclick.*?class="s xst">(.*?)</a>',re.S);
        result_article = re.findall(pattern_article,html)
        #帖子列表。里面每一个元素是一个帖子。一个帖子是一个字典。
        articles = []
        if result_article:
            for item in result_article:
                # print item
                # exit()
                # continue
                #每一个帖子都是一个字典。包含2个key
                article = {}
                article['href'] = "http://bbs.luanren.com/thread"+item[0]
                article['title'] = item[1]
                #print article
                # print item[1].decode('gbk')
                # continue
                #添加帖子到列表尾部
                articles.append(article)
        return articles
    def get_yuer(self):
        html = urllib.urlopen("http://bbs.luanren.com/forum.php?mod=forumdisplay&fid=238").read()
        # print(html.decode('gbk'))
        # <a href="http://bbs.luanren.com/forum.php?mod=viewthread&amp;tid=5591445&amp;extra=" target="_blank" class="xst">男人常吃豆腐 精子“减产”</a>
        pattern_article = re.compile('<a href="http://bbs.luanren.com/thread(.*?)".*?onclick.*?class="s xst">(.*?)</a>',re.S);
        result_article = re.findall(pattern_article,html)
        #帖子列表。里面每一个元素是一个帖子。一个帖子是一个字典。
        articles = []
        if result_article:
            for item in result_article:
                # print item
                # exit()
                # continue
                #每一个帖子都是一个字典。包含2个key
                article = {}
                article['href'] = "http://bbs.luanren.com/thread"+item[0]
                article['title'] = item[1]
                #print article
                # print item[1].decode('gbk')
                # continue
                #添加帖子到列表尾部
                articles.append(article)
        return articles


    def test(self):
        req2 = urllib2.Request(Liuanren.home_url)
        result2 = self.opener.open(req2)
        print(result2.read().decode('gbk'))
if __name__ == '__main__':
    pass