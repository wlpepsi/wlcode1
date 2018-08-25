
import random
import os
from lxml import etree
import requests

IPS = """HTTPS://222.125.215.89:80
HTTP://118.190.95.35:9001
HTTP://61.135.217.7:80
HTTPS://120.24.152.123:3128
HTTP://219.141.153.41:80
HTTP://118.190.95.43:9001
HTTP://123.232.175.186:8118
HTTPS://121.231.156.161:8088
HTTP://111.155.116.217:8123
HTTPS://117.43.1.252:808
HTTP://111.172.3.152:8118
HTTPS://115.219.104.156:8010"""

class GetIp(object):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    }
    base_url = 'http://www.xicidaili.com/nn/{}'
    test_url='https://bbs.51credit.com/forum-202-1.html'

    def check_url(self,key):
        index = key.find(':')
        proxy = {
            key[:index]: key[index + 1:]
        }
        response1 = requests.get(url=self.test_url, headers=self.headers, proxies=proxy)
        return True if response1.status_code == 200 else False

    def to_txt(self):
        fp=open('ippool1.txt','a')

        for i in range(1, 2):
            response = requests.get(url=self.base_url.format(i), headers=self.headers)
            html_str = response.text
            etreeobj = etree.HTML(html_str)
            tr_list = etreeobj.xpath('//table/tr')
            for tr in tr_list[1:]:
                ip = tr.xpath('./td[2]/text()')[0]
                port = tr.xpath('./td[3]/text()')[0]
                style = tr.xpath('./td[6]/text()')[0]
                key = style + '://' + ip + ':' + port
                if self.check_url(key):
                    fp.write(key+'\n')
        fp.close()

    def get_ip(self):
        return random.choice(IPS.split('\n'))