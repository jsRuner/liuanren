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
import urllib,urllib2,os,json,cookielib,random
import ConfigParser

# 登录地址
login_url = "http://bbs.luanren.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
# 首页地址
home_url = "http://bbs.luanren.com/"

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
    if not num.isdigit():
        num = 0
    print("当前帖子最后的楼层数为 %s" % num)
    return num

# 获取配置文件信息。
#[('username', 'zhangwenwei'), ('password', 'saoli123')]
# [('username', 'test'), ('password', 'test123')]
def get_config():
    config = ConfigParser.RawConfigParser()
    config.read('robfloors.ini')
    ses = config.sections()
    # print(ses)
    for se in ses:
        # print(se)
        print(config.items(se))
    # print config.get("global", "ip")
    # print config.get("Default", "username")


# 修改配置文件的信息。配置信息。todo：多个账号咋办。
# 3个参数。分组。 索引。值。
def set_config(se,key,value):
    config = ConfigParser.ConfigParser()
    config.read('robfloors.ini')
    #看是否存在该Section，不存在则创建
    if not config.has_section(se):
        config.add_section(se)
    config.set(se, key, value)
    # 写入文件
    config.write(open('robfloors.ini', "w"))

#登录操作。需要账号与密码。 这里不需要保存cookie.
def login_bbs(username,password):
    data = {
        "quickforward": "yes",
        "handlekey": "ls",
        "username": username,
        "password": password
    }  # urllib进行编码。
    post_data = urllib.urlencode(data)
    # 初始化一个CookieJar来处理Cookie。
    ckjar = cookielib.CookieJar()
    ckproc = urllib2.HTTPCookieProcessor(ckjar)
    # 实例化一个全局opener。
    opener = urllib2.build_opener(ckproc)
    # 获取cookie。
    req = urllib2.Request(login_url, post_data)
    opener.open(req)
    return opener

# 获取帖子的回复信息。主要是表单的formhash
# 需要传递登录过的opener. 帖子的url
def get_replyinfo(opener, topic_url):
    xx = opener.open(urllib2.Request(topic_url))
    topic_html = xx.read()
    pattern = re.compile('<input type="hidden" name="formhash" value="(.*?)" />', re.S)
    formhashs = re.findall(pattern, topic_html)
    formhash = False
    if formhashs:
        for item in formhashs:
            formhash = item
            print(u"表单formhash = %s" %item)  # 901ec69e
            break #找到了就停止循环
    #未找到则返回
    if not formhash:
        return {"status": False}
    # 解析参数.判断url是否存在tid。如果不存在，则执行正则
    result = urlparse.urlparse(topic_url)
    tid = False #默认tid为 False
    #如果是url不携带参数。
    if result.query == "":
        pattern = re.compile(".*?thread-(.*?)-\d-\d.html", re.S)
        result = re.findall(pattern, topic_url)
        if result:
            tid = result[0]
    else: #携带了参数。
        urlparse.parse_qs(result.query, True)
        params = urlparse.parse_qs(result.query, True)
        tid = params['tid'][0]
    #没有tid。则返回。
    if not tid:
        return {"status": False}
    # fid 是什么还不确定。
    fid_url = False
    fid = False
    pattern2 = re.compile('<span class="pgb y"><a href="(.*?)">.*?</a></span>', re.S)
    result2 = re.findall(pattern2, topic_html)
    #从页面中获取fid_url
    if result2:
        fid_url = result2[0]
    if fid_url:#匹配到fid_url。则进入解析。
        # 解析fid
        result3 = urlparse.urlparse(fid_url)
        if result3.query == "":
            return {"status": False}
        else:
            params3 = urlparse.parse_qs(result3.query, True)
            fid = params3['fid'][0]
    #没有fid ,则返回
    if not fid:
        return {"status": False}
    print(u"解析的fid = %s " %fid)
    reply_url = "http://bbs.luanren.com/forum.php?mod=post&action=reply&fid=" + fid + "&tid=" + tid + "&extra=page\%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1"
    return {"formhash": formhash, "reply_url": reply_url,"status":True}

# 回复帖子。需要登录操作。需要回复帖子。
#需要帖子回复的地址。表单formhash,回复的内容。todo:需要改进。判断 是否回复成功。
def reply_topic(opener, reply_url, formhash, msg):
    headers = {
        # "Referer": "http://bbs.168hs.com/forum.php?mod=post&action=newthread&fid=159",
        "Host": "bbs.luanren.com",
    }
    data = {
        "formhash": formhash,
        "posttime": time.time(),
        "message": msg.encode('gbk')
    }
    # urllib进行编码。
    post_data = urllib.urlencode(data)
    req3 = urllib2.Request(reply_url, post_data, headers)
    rs = opener.open(req3)
    #判断是否回复ok. 回复发布成功
    print(rs.read().decode('gbk'))
    # #提取中文 todo:失败。下次在尝试。
    # p2 = re.compile(ur'[^\u4e00-\u9fa5]',re.S)
    # result = re.findall(p2,rs.read().decode('gbk'))
    # print(result)
    # if result:
    #     print(" ".join(result))
    # if rs.read().find("成功") == -1:
    #     print(u"回复失败")
    #     return False
    # else:
    #     print(u"回复成功")
    #     return True

#回复帖子主函数。
#需要读取配置文件的账号信息。
#一个线程。只负责一个账号的回复。
#需要一个参数。例如1或者2.表明读取的时哪一个账号。
#该函数。根据配置文件。进行回复帖子。
def replay_main(name):
    #读取配置。
    config = ConfigParser.RawConfigParser()
    config.read('robfloors.ini')
    topic_url = config.get("global","url")
    speed = config.get("global","speed")
    floors = config.get("global","floors")
    if floors =="":
        print(u"没有楼层可以抢")
        exit()
    #如果低于6秒。则修改6
    if int(speed) < 6:
        speed = 6
    speed = float(speed)
    #根据name 读取哪个账号。
    username = config.get("account_%d" % name,"username")
    password = config.get("account_%d" % name,"password")
    status = config.get("account_%d" % name,"status")
    #该账号不再抢楼。
    if int(status) != 1:
        print(u"该账号的状态不为1，不参与抢楼")
        exit()
    msgs = config.get("account_%d" % name,"msgs").split("#") #该账号回复的信息内容
    # print(msgs)
    # print(username)
    # print(password)
    # return
    opener = login_bbs(username, password)
    while True:
        replyinfo = get_replyinfo(opener, topic_url)
        time.sleep(1)
        if not replyinfo['status']:
            print(u'该文章未能获取回复的信息：%s' % topic_url)
            time.sleep(speed)
            continue
        msgindex = random.randint(0, len(msgs) - 1)
        print(msgs[msgindex])
        reply_topic(opener, replyinfo['reply_url'], replyinfo['formhash'],msgs[msgindex].decode('utf-8'))
        time.sleep(speed)

#判断 配置文件中的楼层是否已经 全部被占。
# 获取最后一个楼层。如果该楼层大于 配置文件中的最大值。则表示程序应该停止。
#修改配置文件中的stop参数
def is_stop():
    pass
#修改楼层参数。例如 当前楼层为10.则楼层参数只保留 大于10的参数。
#同时修改速度参数。判断最后楼层与中奖楼层的距离。如果距离很近。则修改速度。
#运算时，需要转换int
def update_floor():
    config = ConfigParser.RawConfigParser()
    config.read('robfloors.ini')
    floors = config.get("global","floors")
    topic_url = config.get("global","url")
    floor_list = []
    #多个楼层时
    if floors.find(",") != -1:
        floor_list = floors.split(",")
    elif floors.isdigit(): #一个楼层时
        floor_list.append(floors)
    else: #没有楼层时
        set_config("global","floors","")
        #应该退出系统。同时修改状态。让其他线程也退出执行。
        exit()
    #获取最后一个楼层。
    last_num = get_lastnum(topic_url)
    #过滤掉低于 最后楼层。
    new_floor_list = [ i for i in floor_list if int(i) > int(last_num)]
    #进行一次排序。
    new_floor_list.sort()
    #获取最小中奖楼层。
    min_floor = new_floor_list[0]
    #转为字符串，存入配置。
    temp = ",".join(new_floor_list)
    set_config("global","floors",temp)

    #更新速度参数。差值低于 5。则修正速度为 6秒一次。否则为2.5分一次。
    if (int(min_floor)- int(last_num)) <= 5:
        speed = 6
    else:
        speed = 60*2+30
    set_config("global","speed",speed)

# 抢楼的线程执行的函数。需要传递特定的账号。回复的信息。进行抢楼操作。

#判断是否中奖的函数。中了则修改配置文件。没中则不操作。 决定账号是否还继续进行回复的操作.

#判断当前的楼层。靠近则修改配置文件。超过了则修改配置文件。 控制回帖的速度。

# 主程序
def main():
    # get_username("http://bbs.luanren.com/forum.php?mod=viewthread&tid=4139087",200)
    # get_username("http://bbs.luanren.com/forum.php?mod=viewthread&tid=4139087&page=1#pid5107373",200)
    # get_lastnum("http://bbs.luanren.com/forum.php?mod=viewthread&tid=4139087")
    # get_lastnum("http://bbs.luanren.com/thread-5591889-1-1.html")
    # replay_main("http://bbs.luanren.com/thread-5592491-1-1.html")
    # replay_main("http://bbs.luanren.com/thread-5591704-1-1.html")
    # get_config()
    # set_config("zhanghao1","username","test")
    # set_config("zhanghao1","password","test123")
    # get_config()
    # update_floor()
    # replay_main(1)
    # replay_main(2)

    my_thread = MyThread(replay_main,1)
    my_thread1 = MyThread(replay_main,2)
    my_thread.start()
    my_thread1.start()
    my_thread.join()
    my_thread1.join()
    pass


if __name__ == '__main__':
    main()