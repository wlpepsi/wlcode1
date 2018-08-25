# -*- coding: utf-8 -*-
# encoding=utf-8


import scrapy, re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import Credit51Item
from ..get_indexurl import get_allpart_indexurl


class Credit51spiderSpider(CrawlSpider):
    name = 'credit51spider'
    allowed_domains = ['bbs.51credit.com']
    start_url = 'http://bbs.51credit.com/'
    start_urls = get_allpart_indexurl(start_url)

    rules = (
        # 抽取每一页的link
        Rule(LinkExtractor(allow=r'forum-\d+-\d\.html'), follow=False),
    )

    # 起始页的解析
    def parse_start_url(self, response):
        tbodys=response.xpath('//tbody[contains(@id,"thread")]')

        for tbody in tbodys:
            item=Credit51Item()

            # 帖子主题
            tit = tbody.xpath('./tr/th/a[1]/text()').extract_first(default=False) or tbody.xpath('./tr/th/a[2]/text()').extract_first(default=False)

            # 帖子超链接
            title_base_url = tbody.xpath('./tr/th/a[1]/@href').extract_first(default=False) or tbody.xpath('./tr/th/a[2]/@href').extract_first(default=False)
            tit_url = 'https://bbs.51credit.com/' + title_base_url

            # 帖子作者
            pst_aut = tbody.xpath('./tr/td[@class="by"][1]/cite/a/text()').extract_first(default=False)

            # 作者链接
            author_base_url = tbody.xpath('./tr/td[@class="by"][1]/cite/a/@href').extract_first(default=False)
            aut_url = 'https://bbs.51credit.com/' + author_base_url

            # 发布时间
            rel_tim = tbody.xpath('./tr/td[@class="by"][1]/em/span/span/@title').extract_first(
                default=False) or tbody.xpath('./tr/td[@class="by"][1]/em/span/text()').extract_first(default=False)

            # 最新留言人
            new_com_aut = tbody.xpath('./tr/td[@class="by"][2]/cite/a/text()').extract_first(default=False)

            # 最新留言时间
            new_com_tim = tbody.xpath('./tr/td[@class="by"][2]/em/a/span/@title').extract_first(default=False)

            # 帖子具体分类
            # 大版块
            ct1 = tbody.xpath('//div[@class="z"]/a[3]/text()').extract_first(default=False)
            # 分区版块
            ct2 = tbody.xpath('//div[@class="z"]/a[4]/text()').extract_first(default=False)

            # 帖子id
            try:
                pid = tbody.xpath('./@id').extract_first(default=False).split('_')[-1]
            except:
                pid = False

            item['pid'] = pid
            item['ct1'] = ct1
            item['ct2'] = ct2
            item['tit'] = tit
            item['tit_url'] = tit_url
            item['pst_aut'] = pst_aut
            item['aut_url'] = aut_url
            item['rel_tim'] = rel_tim
            item['new_com_aut'] = new_com_aut
            item['new_com_tim'] = new_com_tim

            yield scrapy.Request(url=tit_url, callback=self.parse_card, meta={'item': item})


    # 回调函数
    def parse_item(self, response):
        normal_tbodys = response.xpath('//tbody[contains(@id,"normalthread")]')

        for tbody in normal_tbodys:
            item = Credit51Item()

            # 帖子主题
            tit = tbody.xpath('./tr/th/a[1]/text()').extract_first(default=False)

            # 帖子超链接
            title_base_url = tbody.xpath('./tr/th/a[1]/@href').extract_first(default=False)
            tit_url = 'https://bbs.51credit.com/' + title_base_url

            # 帖子作者
            pst_aut = tbody.xpath('./tr/td[@class="by"][1]/cite/a/text()').extract_first(default=False)

            # 作者链接
            author_base_url = tbody.xpath('./tr/td[@class="by"][1]/cite/a/@href').extract_first(default=False)
            aut_url = 'https://bbs.51credit.com/' + author_base_url

            # 发布时间
            rel_tim = tbody.xpath('./tr/td[@class="by"][1]/em/span/span/@title').extract_first(
                default=False) or tbody.xpath('./tr/td[@class="by"][1]/em/span/text()').extract_first(default=False)

            # 最新留言人
            new_com_aut = tbody.xpath('./tr/td[@class="by"][2]/cite/a/text()').extract_first(default=False)

            # 最新留言时间
            new_com_tim = tbody.xpath('./tr/td[@class="by"][2]/em/a/span/@title').extract_first(default=False)

            # 帖子具体分类
            # 大版块
            ct1 = tbody.xpath('//div[@class="z"]/a[3]/text()').extract_first(default=False)
            # 分区版块
            ct2 = tbody.xpath('//div[@class="z"]/a[4]/text()').extract_first(default=False)

            # 帖子id
            try:
                pid = tbody.xpath('./@id').extract_first(default=False).split('_')[-1]
            except:
                pid = False

            item['pid'] = pid
            item['ct1'] = ct1
            item['ct2'] = ct2
            item['tit'] = tit
            item['tit_url'] = tit_url
            item['pst_aut'] = pst_aut
            item['aut_url'] = aut_url
            item['rel_tim'] = rel_tim
            item['new_com_aut'] = new_com_aut
            item['new_com_tim'] = new_com_tim

            yield scrapy.Request(url=tit_url, callback=self.parse_card, meta={'item': item})

    def parse_card(self, response):

        item = response.meta['item']

        # 每一个评论的div标签
        divs = response.xpath('//div[@id="postlist"]/div[contains(@id,"post")]')
        for div in divs[:-1]:
            # 评论作者
            com_aut = div.xpath('.//div[@class="authi"]/a/text()').extract_first(default=False)

            # 评论作者的注册时间
            aut_rel_tim = div.xpath('.//dl[@class="pil cl"]/dd[5]/text()').extract_first(default=False)

            # 评论作者的url
            com_aut_url = 'https://bbs.51credit.com/' + div.xpath('.//div[@class="authi"]/a/@href').extract_first(
                default=False)

            # 评论的内容
            pattern = re.compile('^\(function\(\).*}\)\(\);', re.S)

            post_contents = div.xpath('.//td[contains(@id,"postmessage")]//text()').extract()
            post_content = ''.join(post_contents).strip()

            # 剔除抓取的js代码
            com = re.sub(pattern, '', post_content)

            # 评论的唯一id，用于判断更新
            cid = div.xpath('./@id').extract_first(default=False).split('_')[-1]

            # 楼层
            number=div.xpath('.//div[@class="pi"]/strong/a/em/text()').extract_first(default=False)
            try:
                flr=number+u'楼'
            except:
                flr=False

            item['com_aut'] = com_aut
            item['aut_rel_tim'] = aut_rel_tim
            item['com_aut_url'] = com_aut_url
            item['com'] = com
            item['cid'] = cid
            item['flr']=flr


            yield item
