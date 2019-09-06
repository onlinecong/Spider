# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import redis
import requests

class BossproDownloaderMiddleware(object):

    # 定义一个成员变量用于提取代理
    def get_ippool(self):
        rds = redis.StrictRedis(host="www.fanjianbo.com",port=6379,db=6)
        ip_list = rds.lrange("ippool",0,rds.llen("ippool"))
        return ip_list
    def process_request(self, request, spider):
        print("中间件.....")
        # 取出代理池
        ip_list = self.get_ippool()
        print(ip_list)
        for ip in ip_list:
            try:
                # 检查代理是否能用
                # requests.get(url="https://www.baidu.com/", headers={"user-agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}, proxies={"https": ip})
                print("当前代理为：",ip)
                # 给当前的request设置代理服务器
                request.meta["proxy"] = "https://"+ip.decode("utf8")
                break
            except Exception  as e:
                print("代理%s已经过期！"%ip)

    def process_response(self, request, response, spider):

        return response

