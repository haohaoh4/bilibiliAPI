import requests
import re
import bili

def get_click(av):
    aid = bili.get_aid(av)
    cid = bili.get_cid(av)
    if aid == bili.cannot_open:
        raise IOError("Internet_error")
    if aid==bili.have_no:
        return bili.have_no
    if aid==bili.have_error:
        raise IOError("None_reason_error")
        #This is a problem on bilibili,have no reasons
    url = "http://interface.bilibili.com/player?id=cid:%s&aid=%s" % (cid,aid)
    text = requests.get(url, bili.headers).content
    click_p = text.find("<click>") + 7
    click_t = re.findall(r'(\w*[0-9]+)\w*', text[click_p:click_p + 30])
    #print aid,cid
    try:
        click = int(click_t[0])
    except IndexError:
        return bili.have_error
        #This is a problem on bilibili,have no reasons
    return click
