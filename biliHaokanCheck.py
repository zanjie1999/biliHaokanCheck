# coding=utf-8

# 检查哔哩哔哩用户在好看视频中被盗的视频
# Sparkle
# v1.0

import httpx
from urllib import parse

# 个人主页的network中搜索 search?mid=
biliMid = 9992930


def getBiliVlist(mid):
    pn = 1
    out = []
    while True:
        data = httpx.get("https://api.bilibili.com/x/space/arc/search?mid={}&ps=100&pn={}&jsonp=jsonp".format(mid, pn))
        j = data.json()
        if j['code'] != 0:
            print(j['message'])
            return
        elif j['data']['list']['vlist']:
            out.extend(j['data']['list']['vlist'])
            pn = pn + 1
            break
        else:
            break
    return out


def searchHaokan(keyword):
    data = httpx.get("http://haokan.hao123.com/web/search/api?pn=1&type=video&query=" + parse.quote(keyword))
    j = data.json()
    if j['errno'] != 0:
        print(j['errmsg'])
        return
    else:
        return j['data']['list']


if __name__ == '__main__':
    txt = ""
    for bv in getBiliVlist(biliMid):
        haokanUrl = []
        bvTitle = bv['title'].strip()
        for hk in searchHaokan(bv['title']):
            if hk['title'].strip == bvTitle:
                haokanUrl.append(hk['url'])
        if haokanUrl:
            out = "{}\n{}\n{}\n".format(
                bv['title'],
                'https://www.bilibili.com/video/' + bv['bvid'],
                '\n'.join(haokanUrl)
            )
            print(out)
            txt = txt + out
        
    if txt:
        with open("bvhk.txt", 'w') as f:
            f.write(txt)

