#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# coding:utf-8
#  tvtest.py
#  测试m3u8的可下载性，基本的直播可用性测试。
#  Copyright 2018 ququ
import datetime
import sys
import urllib
import urllib3
import urlparse
import time
import os
import re
import pprint
import json
from pyquery import PyQuery as pq

headers = {
    'Host': 'mxtoolbox.com',
    'Origin': 'https://mxtoolbox.com',
    'X-Requested-With': 'XMLHttpRequest',
    'MasterTempAuthorization': 'f67aac26-fe12-4a9c-b1c2-771db0816033',
    'Content-Type': 'application/json; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cookie': ''}
# urlDNSlookup 是在线DNS网站，没事可以自已多找找然后按网站返回数据改代码。
urlDNSlookup = 'https://mxtoolbox.com/Public/Lookup.aspx/DoLookup2'


def gethosts():
    if len(sys.argv) != 2:
        print("arg error, " + sys.argv[0] + " input hosts file")
        exit(1)
    input_file = sys.argv[1]
    hinFile = open(input_file, "r+")
    print('get ipv6 for the hosts in ' + input_file)
    output_file = input_file + "-new"
    error_file = input_file + "-err"
    houtFile = open(output_file, "w")
    herrorFile = open(error_file, "w")

    L = 0
    FileList = hinFile.readlines()
    FileList2 = []
    for Line0 in FileList:
        if Line0[0] != '#' and len(Line0) > 2:
            position = Line0.index(' ')
            Line1 = Line0[position:]
            # print(position)
            position2 = Line1.find('#')
            # print(position2)
            if position2 > 0:
                strhost = Line1[1:position2 - 1]
            else:
                strhost = Line1[1:len(Line1) - 1]
            # print("the host is: %s: " +strhost)
            url = urlDNSlookup
            dataraw = '{"inputText":"aaaa:' + strhost + '","resultIndex":4}'
            # data = urllib.urlencode(dataraw)
            print(dataraw)
            # print(data)
            try:
                # response = urllib2.urlopen('https://mxtoolbox.com/')
                request = urllib2.Request(url, data=dataraw, headers=headers)
                # request = urllib2.Request(url,headers = headers)
                response = urllib2.urlopen(request)
                text = response.read()
                # text = unicode(response.read(),"utf-8")
                # 找tAAAA\\t
                p1 = text.find("AAAA\\\\t")
                if p1 > 0:
                    p2 = text.find(",", p1)
                    stripv6 = text[p1 + 7:p2]
                    Lineout = stripv6 + ' ' + strhost + '\n'
                    houtFile.writelines(Lineout)
                else:
                    stripv6 = "error"
                    Lineout = stripv6 + ' ' + strhost + '\n'
                    herrorFile.writelines(Lineout)
                print(Lineout)
            except urllib2.URLError as e:
                print
                "Error: %s, url: %s" % (e, url)

    herrorFile.close()
    houtFile.close()
    hinFile.close()
    print('done\n')


if __name__ == '__main__':
    gethosts()
