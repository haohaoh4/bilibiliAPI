import requests
import re
cannot_open = -1
have_no = -2
have_error = -3
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
def get_id(av):
	url = "http://bilibili.com/video/av%s" % av
	text = requests.get(url, headers)
	if (str(text) != "<Response [200]>"):
		return cannot_open
	text = text.content
	if text.find("error.css") > 0:
		return have_no
	pid_p = text.find('EmbedPlayer(\'player\', "//static.hdslb.com/play.swf", "cid=')
	return re.findall(r'(\w*[0-9]+)\w*', text[pid_p:pid_p + 80])
def get_aid(av):
	id = get_id(av)
	if id == cannot_open:
		return -1
	if id == have_no:
		return 0
	try:
		return id [1]
	except IndexError:
		return have_error
def get_cid(av):
	id = get_id(av)
	if id == cannot_open:
		return -1
	if id == have_no:
		return 0
	try:
		return id[0]
	except IndexError:
		return have_error



#a api about lots of info : url = \
#    "http://api.bilibili.com/x/web-interface/archive/stat?callback=jQuery172026117636432635716_1503748455511&" \
#    "aid=%s&jsonp=jsonp&_=1503748456436"