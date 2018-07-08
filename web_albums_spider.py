#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @version: python 2.7.13
# @author: baorunchen(runchen0518@gmail.com)
# @date: 2018/7/5


import requests
import urllib2
from bs4 import BeautifulSoup
import re
import os.path

weibo_uid_list = []
douban_uid_list = []
douban_albums_uri_list = []

cookie = {
    "Cookie": ''
}

headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'cookie': cookie
}


def get_weibo_albums_uri(url):
    page_data = requests.get(url, cookies=cookie).content

    pattern = re.compile(
        u'<a title="微博配图".*?undefined="">', re.S)
    result = re.findall(pattern, page_data)
    print result


def collect_douban_albums_uri(url):
    page = requests.get(url, headers, timeout=30)
    page.encoding = page.apparent_encoding
    page_data = page.text
    soup = BeautifulSoup(page_data, 'html.parser')
    album_list = soup.find_all('div', 'albumlst')
    pattern = re.compile('<a class="album_photo" href=".*?">', re.S)
    items = re.findall(pattern, str(album_list))
    data = items[-1].split()[-1].split('href="')[-1].split('">')
    album_uri = data[0]
    douban_albums_uri_list.append(album_uri)


def douban_albums_spider(uri, page_num):
    get_douban_next_album_uri(uri)

    print '正在爬取网址：%s' % uri
    page = requests.get(uri, headers, timeout=30)
    page.encoding = page.apparent_encoding
    page_data = page.text
    soup = BeautifulSoup(page_data, 'html.parser')
    pic_list = soup.find_all('div', 'photo_wrap')
    pattern = re.compile('<a class="photolst_photo" href=".*?" title="">', re.S)
    items = re.findall(pattern, str(pic_list))
    pic_num = 1
    for item in items:
        print '第%s张图片' % pic_num
        download_douban_pic(item.split()[2].split('href="')[-1].split('"')[0] + 'large', page_num, pic_num)
        pic_num += 1

    print '爬取完毕！\n'


def download_douban_pic(uri, page_num, pic_num):
    page = requests.get(uri, headers, timeout=30)
    page.encoding = page.apparent_encoding
    page_data = page.text
    soup = BeautifulSoup(page_data, 'html.parser')
    pic_list = soup.find_all('table', 'pic-wrap')
    pattern = re.compile('src=".*?"', re.S)
    item = re.search(pattern, str(pic_list))
    if item is not None:
        pic_uri = item.group(0).split('"')[1]
        down_image(pic_uri, "douban_ftt_page%s_pic%s.jpg" % (page_num, pic_num))


def down_image(url, file_name):
    global headers
    req = urllib2.Request(url=url, headers=headers)
    binary_data = urllib2.urlopen(req).read()
    douban_pic_dir = os.getcwd() + '/douban_pic/'
    if not os.path.exists(douban_pic_dir):
        os.mkdir(douban_pic_dir)
    temp_file = open(douban_pic_dir + file_name, 'wb')
    temp_file.write(binary_data)
    temp_file.close()


def get_douban_next_album_uri(uri):
    page = requests.get(uri, headers, timeout=30)
    page.encoding = page.apparent_encoding
    page_data = page.text
    soup = BeautifulSoup(page_data, 'html.parser')
    next_page = soup.find_all('span', 'next')
    pattern = re.compile('href=".*?"', re.S)
    item = re.search(pattern, str(next_page))
    if item is not None:
        next_uri = item.group(0).split('"')[1]
        douban_albums_uri_list.append(next_uri)


def read_weibo_uid_from_txt():
    with open('weibo_uri.txt', 'r') as fp:
        data = fp.readlines()
    for uid in data:
        if uid.strip('\n').isdigit():
            weibo_uid_list.append(int(uid.strip('\n')))


def read_douban_uid_from_txt():
    with open('douban_uri.txt', 'r') as fp:
        data = fp.readlines()
    for uid in data:
        if uid.strip('\n').isdigit():
            douban_uid_list.append(int(uid.strip('\n')))


def process_weibo():
    read_weibo_uid_from_txt()
    for uid in weibo_uid_list:
        weibo_album_uri = 'http://photo.weibo.com/%s/albums?rd=1' % uid
        print weibo_album_uri
        get_weibo_albums_uri(weibo_album_uri)
        continue


def process_douban():
    read_douban_uid_from_txt()
    for uid in douban_uid_list:
        douban_album_uri = 'https://www.douban.com/people/%s/photos' % uid
        collect_douban_albums_uri(douban_album_uri)

    page_num = 1
    while len(douban_albums_uri_list) != 0:
        uri = douban_albums_uri_list[0]
        douban_albums_spider(uri, page_num)
        douban_albums_uri_list.remove(uri)
        page_num += 1


def main():
    # process_weibo()
    process_douban()


if __name__ == '__main__':
    main()
