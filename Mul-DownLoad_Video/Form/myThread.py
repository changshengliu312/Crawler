# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests, sys,re,json
from urllib import request
import os,random,urllib,m3u8
import threading,time

class myThread(threading.Thread):
    def __init__(self,url,filename):
        threading.Thread.__init__(self)
        self.url = url
        self.filename = filename

    def run(self):
        urllib.request.urlretrieve( url=self.url, filename=self.filename, reporthook=self.Schedule )
        print('%s下载完成.'%self.filename)

    def Schedule(self, a, b, c):
        per = 100.0 * a * b / c
        if per > 100:
            per = 1
        sys.stdout.write( "  " + "%.2f%% 已经下载的大小:%ld 文件大小:%ld" % (per, a * b, c) + '\r' )
        sys.stdout.flush()