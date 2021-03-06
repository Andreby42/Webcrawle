#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
###################################################
#import os
#import sys
#print sys.path
#skyeyepath = os.path.realpath((os.path.dirname(__file__)) + "/../")  #将当前的路径加入path
#if not skyeyepath in sys.path:
#    sys.path.append(skyeyepath)

import ConfigParser  #INI读取数据
import time


import VVQueue  #消息队列维护
import VVSpider  #爬虫
import VVCms  #CMS识别
import Cclose_open  #结束进程  在从新开启进程

INT_TX_Queue = 1  # 消息队列维护线程
INT_TX_cms = 5    # cms识别线程 建议一个CPU 10个线程 n*10
INT_TX_spider = 2  # 设置采集线程

if __name__ == '__main__':
    try:
        config = ConfigParser.ConfigParser()
        config.readfp(open("Server.ini"))
        INT_TX_Queue = int(config.get("DATA", "TX_Queue"))  # 消息队列维护线程
        INT_TX_cms = int(config.get("DATA", "TX_cms"))      # cms识别o线程
        INT_TX_spider = int(config.get("DATA", "TX_openrul"))  # 设置采集线程
    except:
        pass

    #结束进程  在从新开启进程
    Cclose_open_threads = []  #线程
    for i in range(1):  #nthreads=10  创建10个线程
        Cclose_open_threads.append(Cclose_open.CS_close_open())
    for thread in Cclose_open_threads:   #不理解这是什么意思    是结束线程吗
        thread.start()  #start就是开始线程

#    # 启动数据库,只能用一个实例，不然数据库压力他打
#    dbinstance = VVQueue.VVQueue(0)
#    dbinstance.start()
    threads0 = []  #线程   消息队列维护
    for i in range(INT_TX_Queue):
        threads0.append(VVQueue.VVQueue(i))
    for t in threads0:
        time.sleep(1)
        t.start()

    # 启动爬虫
    spiderthreads = []  #线程  数据采集
    for i in xrange(INT_TX_spider):
        t = VVSpider.VVSpider(i)
        spiderthreads.append(t)
        time.sleep(0.01)
        t.start()

    # 线程cms识别
    cmsthreads = []  # 线程cms识别
    for i in xrange(INT_TX_cms):  # nthreads=10  创建10个线程
        t = VVCms.VVCms(i)
        cmsthreads.append(t)
        time.sleep(0.01)
        t.start()


    # 等待
    # 给一个初始的域名
#    VVQueue.ReadQueue.put('www.sina.com.cn')
#    VVQueue.ReadQueue.put('www.163.com')
#    VVQueue.CmsQueue.put('zysd.com.cn')
#    VVQueue.CmsQueue.put('www.baidu.com')
#    VVQueue.CmsQueue.put('domeng.cn')
#    VVQueue.CmsQueue.put('soxan.cn')
#    VVQueue.CmsQueue.put('chinahanhai.net')
    #dbinstance.join()
#    while True:
#        time.sleep(0.5)


