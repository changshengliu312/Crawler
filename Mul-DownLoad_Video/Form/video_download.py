# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests, sys,re,json
from urllib import request
import os,random,urllib,m3u8

class VideoCrawler():
    """
    函数说明:初始化
    """
    def __init__(self):
        self.url = 'http://www.iqiyi.com/v_19rr7qhfg0.html#vfrm=19-9-0-1'
        self.m3u8_file_url = 'http://cache.utovr.com/201508270528174780.m3u8 '
        self.proxy_url = 'http://www.xicidaoli.co,/nn/'
        self.filename = 'Video'

        self.down_path = r'C:\Users\v_liucshliu\PycharmProjects\learn\GUI-DownLoad_Video'
        self.final_path = r'C:\Users\v_liucshliu\PycharmProjects\learn\GUI-DownLoad_Video'
        self.headrs = [(
            'User-agent',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36')]

    """
    函数说明:获取代理列表
    """
    def get_ip_list(self,proxy_url):
        print("正在获取代理列表...")
        html = requests.get(url=proxy_url,headers=self.headrs).text
        soup = BeautifulSoup(html,'lxml')
        ips = soup.find(id='ip_list').find_all('tr')
        ip_list = []
        for i in range(1,len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            ip_list.append(tds[1].text + ':' +tds[2].text)
        print("代理列表抓取成功.")
        return ip_list

    """
    函数说明:获取代理ip
    """
    def get_random_ip(self,ip_list):
        print('正在设置随机代理...')
        proxy_list = []
        for ip in ip_list:
            proxy_list.append('http://'+ip)
        proxy_ip = random.choice(proxy_list)
        proxies = {'http':proxy_ip}
        print('代理设置成功.')
        return proxies

    """
    函数说明:解析m3u8文件,获取下载url_list
    """

    def parse_m3u8(self):
        m3u8_obj = m3u8.load(self.m3u8_file_url)  # this could also be an absolute filename
        #print(m3u8_obj.segments.uri)
        #print(m3u8_obj.target_duration)
        target = m3u8_obj.segments.uri

        return target

    """
    函数说明:回调函数，打印下载进度
    """
    def Schedule(self,a, b, c):
        per = 100.0 * a * b / c
        if per > 100:
            per = 1
        sys.stdout.write("  " + "%.2f%% 已经下载的大小:%ld 文件大小:%ld" % (per, a * b, c) + '\r')
        sys.stdout.flush()

    """
    函数说明:文件下载
    """
    def video_download(self,url_list):
        # 这是代理IP proxy = {'http': '117.68.192.78:18118'}
        # 创建ProxyHandler  r = requests.get(url,proxies=proxies)
        #proxy_support = request.ProxyHandler(proxy)
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = self.headrs
            urllib.request.install_opener(opener)
        except:
            print('add header info failed..')
        else:
            print('unknow error')

        filename_num = 0
        for i in range(len(url_list)):
            filename_num = filename_num+1
            self.filename = self.filename +str(filename_num)+'.ts'
            print('%s下载中:' % self.filename)
            urllib.request.urlretrieve(url=url_list[i], filename=self.filename,reporthook=self.Schedule)
        print('\n下载完成！')
        #request.urlretrieve(url=url, filename=filename,reporthook=Schedule)

    """
    函数说明:文件合并
    """
    def merge(self):
        os.system('copy/b %s\\*.ts %s\\new.ts'%(self.down_path,self.final_path))
        files = os.listdir(self.down_path)
        for filena in files:
            del_file = self.down_path + '\\' + filena
            os.remove(del_file)
        print('合并完成!')

# if __name__ == '__main__':
#     filename ='video'
#     download_video = VideoCrawler()
#     url_list = download_video.parse_m3u8()
#     for i in range(len(url_list)):
#         print(url_list[i])
#     download_video.video_download(url_list,filename)
#     download_video.merge()
