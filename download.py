import os
import requests
 
def download(url):
    download_path = '/root/AndroidHeatMap/download/'
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    all_content = requests.get(url).text
    file_line = all_content.split("\n")
    
    if file_line[0] != "#EXTM3U":
        raise BaseException(u"not M3U8link")
    else:
        unknow = True
        for index, line in enumerate(file_line):
            if "EXTINF" in line:
                unknow = False
                pd_url = url.rsplit("/", 1)[0] + "/" + file_line[index + 1]
                res = requests.get(pd_url)
                c_fule_name = str(file_line[index + 1])
                with open(download_path + "/" + c_fule_name, 'ab') as f:
                    f.write(res.content)
                    f.flush()
        if unknow:
            raise BaseException("cannot find link")
        else:
            print("finish downloading")
 
if __name__ == '__main__':
    url = 'https://jjdong5.com/get_file/4/1fa69b06c6276768e95cc0c04d85feec693488a588/13000/13287/13287_360p.m3u8'
    download(url)
