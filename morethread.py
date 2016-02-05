#/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import time

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

def print_time(counter) :
    while counter :
        print "counter = %d" % counter
        counter -= 1
        time.sleep(1)
def print_timestr(list):
    counter = list[0]
    while counter :
        print "name=%s counter = %d" % (list[1],counter)
        counter -= 1
        time.sleep(1)


def main() :
    my_thread = MyThread(print_timestr, (10,u"线程"))
    my_thread1 = MyThread(print_timestr, (10,u"线程1"))


    my_thread.start()
    my_thread1.start()



    my_thread.join()
    my_thread1.join()

if __name__ == '__main__':
    main()