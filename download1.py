# -*- coding:utf-8 -*-  
import os
import sys
import requests
import datetime
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
 
reload(sys)
sys.setdefaultencoding('utf-8')
 
def download(url):
    download_path = os.getcwd() + "\download"
    if not os.path.exists(download_path):
        os.mkdir(download_path)
        
    download_path = os.path.join(download_path, datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    #print download_path
    os.mkdir(download_path)
        
    all_content = requests.get(url).text
    if "#EXTM3U" not in all_content:
        raise BaseException("not a M3U8 link")
 
    if "EXT-X-STREAM-INF" in all_content:
        file_line = all_content.split("\n")
        for line in file_line:
            if '.m3u8' in line:
                url = url.rsplit("/", 1)[0] + "/" + line
                all_content = requests.get(url).text
 
    file_line = all_content.split("\n")
 
    unknow = True
    key = ""
    for index, line in enumerate(file_line):
        if "#EXT-X-KEY" in line:
            method_pos = line.find("METHOD")
            comma_pos = line.find(",")
            method = line[method_pos:comma_pos].split('=')[1]
            print "Decode Method：", method
            
            uri_pos = line.find("URI")
            quotation_mark_pos = line.rfind('"')
            key_path = line[uri_pos:quotation_mark_pos].split('"')[1]
            
            key_url = url.rsplit("/", 1)[0] + "/" + key_path
            res = requests.get(key_url)
            key = res.content
            print "key：" , key
            
        if "EXTINF" in line: # find ts addr and download it
            unknow = False
            pd_url = url.rsplit("/", 1)[0] + "/" + file_line[index + 1] # combine ts URL
            #print pd_url
            
            res = requests.get(pd_url)
            c_fule_name = file_line[index + 1].rsplit("/", 1)[-1]
            
            if len(key): # AES descrypt
                cryptor = AES.new(key, AES.MODE_CBC, key)  
                with open(os.path.join(download_path, c_fule_name + ".mp4"), 'ab') as f:
                    f.write(cryptor.decrypt(res.content))
            else:
                with open(os.path.join(download_path, c_fule_name), 'ab') as f:
                    f.write(res.content)
                    f.flush()
    if unknow:
        raise BaseException("cannot find downloading link")
    else:
        print "finish downloading"
    merge_file(download_path)
 
def merge_file(path):
    os.chdir(path)
    cmd = "copy /b * new.tmp"
    os.system(cmd)
    os.system('del /Q *.ts')
    os.system('del /Q *.mp4')
    os.rename("new.tmp", "new.mp4")
    
if __name__ == '__main__': 
    url = 'https://jjdong5.com/get_file/4/1fa69b06c6276768e95cc0c04d85feec693488a588/13000/13287/13287_360p.m3u8'
    download(_url)