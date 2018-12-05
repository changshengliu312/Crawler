# -*- coding:UTF-8 -*-
import re
import requests,os

def download_m3u8(url):
    cmd_str = 'ffmpeg -i \"' + url + '\" ' + '-acodec copy -vcodec copy -absf aac_adtstoasc  output.mp4'
    os.system(cmd_str )

# if __name__ == '__main__':
#         url = 'http://cache.utovr.com/201508270528174780.m3u8'
#         download_m3u8(url)