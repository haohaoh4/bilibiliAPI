import requests
import time
import re
headers = {
            'Host': 'blog.csdn.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://www.baidu.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
        }
def get_click(av):
    url = "http://bilibili.com/video/av%s" % av
    text = requests.get(url, headers)
    if(str(text) != "<Response [200]>"):
        raise Exception("Can't open %s" % url)
    text = text.content
    if text.find("error.css") > 0:
        return -1
    pid_p = text.find('EmbedPlayer(\'player\', "//static.hdslb.com/play.swf", "cid=')
    id = re.findall(r'(\w*[0-9]+)\w*', text[pid_p:pid_p + 80])
    try:
        url = "http://interface.bilibili.com/player?id=cid:%s&aid=%s" % (id[0], id[1])
    except IndexError:
        print "fail in av%s" % av
        return -1
    text = requests.get(url, headers).content
    click_p = text.find("<click>") + 7
    click_t = re.findall(r'(\w*[0-9]+)\w*', text[click_p:click_p + 30])
    click = int(click_t[0])
    return click
