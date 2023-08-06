
from .base_classes import *
from .schedule import CrawlThread,RouteThread,CheckThread
from threading import Thread
from .setting import THREAD_NUM

def run():
    c = CrawlThread(1,"crawl",1)
    r = RouteThread(2,"route",2)

    ch_list = []
    for i in range(THREAD_NUM["check"]):
        ch = CheckThread(i,"check_{}".format(i),i)
        ch_list.append(ch)
    r.start()
    c.start()
    for ch in ch_list:
        ch.start()

    r.join()
    c.join()
    for ch in ch_list:
        ch.join()