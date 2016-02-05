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
import urllib,urllib2,re,json,httplib,time,os,cookielib,urlparse,random,socket
socket.setdefaulttimeout(50)

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
    def get_replyinfo(self,topic_url):
        print(u'获取回帖的信息')
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
    # 获取文化板块
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
    # 获取育儿板块
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

    def guanshui(self):
        return [{'href':"http://bbs.luanren.com/forum.php?mod=viewthread&tid=5236375","title":"shui tie"}]
        # pass
    def get_memberphoto(self):
        # 获取图片。
        html = urllib.urlopen("http://bbs.luanren.com/forum-3-1.html").read()
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
    #获取mm照片。获取的mm帖子，还存在一些遗漏。
    def get_mmphoto(self):
        # 获取图片。
        html = urllib.urlopen("http://bbs.luanren.com/forum.php?mod=forumdisplay&fid=3&typeid=3&typeid=3&filter=typeid&page=2").read()
        # print(html.decode('gbk'))
        # <a href="http://bbs.luanren.com/forum.php?mod=viewthread&amp;tid=5591445&amp;extra=" target="_blank" class="xst">男人常吃豆腐 精子“减产”</a>
        # pattern_article = re.compile('<a href="http://bbs.luanren.com/thread(.*?)".*?onclick.*?class="s xst">(.*?)</a>',re.S);
        pattern_mm = re.compile('<em>.*?MM.*?<a href=\"(.*?)\" onclick.*?class="s xst">(.*?)</a>.*?<cite.*?c="1".*?>(.*?)</a></cite>.*?<td class="num"><a.*?>(\d+)</a><em>(\d+)</em></td>',re.S)
        result_article = re.findall(pattern_mm,html)
        #帖子列表。里面每一个元素是一个帖子。一个帖子是一个字典。
        articles = []
        if result_article:
            for item in result_article:
                regex = re.compile(r'.*?(style|</a>).*?')
                if (re.match(regex,item[0])):
					continue
                # print item
                # exit()
                # continue
                #每一个帖子都是一个字典。包含2个key
                article = {}
                article['href'] = item[0].replace("&amp;","&")
                article['title'] = item[1]
                #print article
                # print item[1].decode('gbk')
                # continue
                #添加帖子到列表尾部
                articles.append(article)
        return articles
    # 获取帖子里的图片地址
    def get_imgsrc(self,topic_url):
        html = urllib.urlopen(topic_url).read()
        # print(html.decode('gbk'))
        # <a href="http://bbs.luanren.com/forum.php?mod=viewthread&amp;tid=5591445&amp;extra=" target="_blank" class="xst">男人常吃豆腐 精子“减产”</a>
        # pattern_article = re.compile('<a href="http://bbs.luanren.com/thread(.*?)".*?onclick.*?class="s xst">(.*?)</a>',re.S);
        pattern_mm  = re.compile('<ignore_js_op>.*?<img id=.*?src=.*? file="(.*?)" class="zoom".*?>.*?</ignore_js_op>',re.S)
        result_article = re.findall(pattern_mm,html)
        #帖子列表。里面每一个元素是一个帖子。一个帖子是一个字典。
        articles = []
        if result_article:
            for item in result_article:
                print item
                # exit()
                # continue
                #每一个帖子都是一个字典。包含2个key
                article = {}
                article['href'] = item

                #添加帖子到列表尾部
                articles.append(article)
        return articles
    # 下载一个帖子里的图片。
    def down_img(self,topic_url):
        # 先获取图片
        imgs = self.get_imgsrc(topic_url)
        filepath = "c:\\liuanren\\"
        for item in imgs:
            print(u"下载图片:%s" % item['href'])
            urllib.urlretrieve(item['href'],filepath+str(time.time() * 1000)+str(random.randint(1,100))+".jpg")
        # pass
    # 保证一个帖子一直处于顶部。当前账号。一小时只能回帖30次。60/30 = 2 分钟。一次。这里保险 2.5分一次
    def keep_top(self,topic_url):
        while True:
            replyinfo = self.get_replyinfo(topic_url)
            if not replyinfo['status']:
                print(u'该文章未能获取回复的信息：%s' % topic_url)
                continue
            msgs = [u"需要这个顶贴机器人，可以联系我。保证你的帖子天天排第一。",u"小手一抖，经验到手。楼主写的不错。2016新年快乐",u"这是神一样的十五个字么我的天啊 标准的十五字回复真是越来越多了 我不会告诉你我是专门来混经验的 呦呦！老夫是神话无可超越的神话～呦 看看我的签名貌似真的很黄很暴力 我想肯定会有人数这句话有多少字 如果你真的不知道有这句话的存在 我觉得此帖必删那我先删前留名了",u"现在的小女孩，十几岁毛还没长齐就和人家xxoo了，到二十多岁的时候不知道换了多少男朋友，一个月好几拨。还他妈无耻的大喊男人侮辱了她的身体，骗了她的心。对于这种女人 我只想说四个字:请联系我",u"小手一抖，经验到手。楼主写的不错。2016新年快乐",u"在看完这帖子以后,我没有立即回复,因为我生怕我庸俗不堪的回复会玷污了这网上少有的帖子.但是我还是回复了,因为觉得如果不能在如此精彩的帖子后面留下自己的网名,那我死也不会瞑目的!能够在如此精彩的帖子后面留下自己的网名是多么骄傲的一件事啊!楼主,请原谅我的自私"]
            msgindex = random.randint(0,len(msgs)-1)
            self.reply_topic(replyinfo['reply_url'],replyinfo['formhash'],msgs[msgindex])
            time.sleep(60*2+30)
    #
    def keep_shui(self,topic_url):
            while True:
                replyinfo = self.get_replyinfo(topic_url)
                time.sleep(5)
                if not replyinfo['status']:
                    print(u'该文章未能获取回复的信息：%s' % topic_url)
                    continue
                msgs = [u"勋章勋章勋章勋章勋章勋章勋章勋章勋章",u"我要勋章 我要勋章 我要勋章",u"冷空气下降，各位坛友注意及时增添衣物..........",u"小手一抖，经验到手。楼主写的不错。2016新年快乐",u"这是神一样的十五个字么我的天啊 标准的十五字回复真是越来越多了 我不会告诉你我是专门来混经验的 呦呦！老夫是神话无可超越的神话～呦 看看我的签名貌似真的很黄很暴力 我想肯定会有人数这句话有多少字 如果你真的不知道有这句话的存在 我觉得此帖必删那我先删前留名了",u"现在的小女孩，十几岁毛还没长齐就和人家xxoo了，到二十多岁的时候不知道换了多少男朋友，一个月好几拨。还他妈无耻的大喊男人侮辱了她的身体，骗了她的心。对于这种女人 我只想说四个字:请联系我",u"小手一抖，经验到手。楼主写的不错。2016新年快乐",u"在看完这帖子以后,我没有立即回复,因为我生怕我庸俗不堪的回复会玷污了这网上少有的帖子.但是我还是回复了,因为觉得如果不能在如此精彩的帖子后面留下自己的网名,那我死也不会瞑目的!能够在如此精彩的帖子后面留下自己的网名是多么骄傲的一件事啊!楼主,请原谅我的自私"]
                msgindex = random.randint(0,len(msgs)-1)
                print(msgs[msgindex])
                self.reply_topic(replyinfo['reply_url'],replyinfo['formhash'],msgs[msgindex])
                time.sleep(60*2+4)
                if msgindex == 2:
                    urllib.urlopen("http://bbs.luanren.com")










    def test(self):
        req2 = urllib2.Request(Liuanren.home_url)
        result2 = self.opener.open(req2)
        print(result2.read().decode('gbk'))
if __name__ == '__main__':
    while True:
        try:
            liuanren = Liuanren()
            liuanren.keep_shui("http://bbs.luanren.com/forum.php?mod=viewthread&tid=5236375")
            print(u"这里不应该执行。。。")
        except Exception,e:
            print(u"出现异常,睡眠10分钟后重新请求")
            time.sleep(60*10)
