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
		return id[1]
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

def get_num_between(text,text1,text2):
	got = re.findall("\d", text[text.find(text1):text.find(text2)])
	ans = 0
	for i in got:
		ans = ans * 10 + int(i)
	return ans

def read_info(aid):
	infoes = {"view":-1,"danmaku":-1,
	    "favorite":-1,"coin":-1,"share":-1,
	    "top":-1,"copyright":False}

	try:
		text = requests.get("http://api.bilibili.com/x/web-interface/archive/stat?"
		                    "aid=%s" % aid)
		if str(text) != "<Response [200]>":
			raise Exception("Can't open http://api.bilibili.com/x/web-interface/archive/stat?aid=%s" % aid)
		if requests.get("http://bilibili.com/video/av%s" % aid).content.find("error.css")>0:
			raise IOError("ERROR")
	except IOError:
		return infoes
	text = text.content
	infoes["view"] = get_num_between(text, 'view', 'danmaku')
	infoes["danmaku"] = get_num_between(text, 'danmaku', 'reply')
	infoes["favorite"] = get_num_between(text, 'favorite', 'coin')
	infoes["coin"] = get_num_between(text, 'coin', 'share')
	infoes["share"] = get_num_between(text, 'share', 'now_rank')
	infoes["top"] = get_num_between(text, 'his-rank', 'no_repaint')
	copyright = get_num_between(text, 'copyright', 'messagre')
	infoes["copyright"] = True if copyright == 2 else False
	return infoes

class video_info:
	def __init__(self):
		self.view = 0
		self.coins = 0
		self.danmaku = 0    #danmaku = danmu
		self.favorite = 0
		self.share = 0
		self.top = 0
		self.copyright = False

def get_video_info(av):
	info = video_info()

	i = read_info(get_aid(av))
	info.coins = i["coin"]
	info.favorite = i["favorite"]
	info.danmaku = i["danmaku"]
	info.share = i["share"]
	info.top = i["top"]
	info.view = i["view"]
	info.copyright = i["copyright"]
	del i
	return info