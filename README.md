# Web Albums Spider

## 爬取网址
[豆瓣相册](https://www.douban.com/)

[微博相册](https://photo.weibo.com/)

## 前期准备

* 在当前文件夹下创建`douban_uri.txt`和`weibo_uri.txt`两个文本文件

* `douban_uri.txt`的每一行存取需要爬取的豆瓣ID

* 在Google Chrome上预先登录好微博，并拿到cookie值

* 在`weibo_uri.txt`第一行存取Google Chrome的微博cookie，下面每一行存取需要爬取的微博ID


## 执行命令

`python web_albums_spider.py`


## 环境配置

* requests
* urllib2
* matplotlib
* BeautifulSoup
* re
* os.path


## 注意事项
* 由于只做了简单的伪装，并没有做代理IP和轮换，所以可能会导致爬取的时候，电脑IP被禁的情况

* 如果针对豆瓣相册爬取较频繁的话，会被豆瓣安全中心感知，识别为异常请求，该爬虫没有对豆瓣做绕登录


## 后续改进
由于单纯为了实现功能，并没有重视代码的性能方面，所以代码可能繁琐并且笨重。后续等功能完成后，针对时间复杂度方面进行相应优化。