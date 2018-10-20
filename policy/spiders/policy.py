import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from policy.items import PolicyItem

class Myspider(scrapy.Spider):

    name = 'policy'
    # allowed_domains = ['http://www.ks.gov.cn/']
    baseurl = "http://www.ks.gov.cn"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.xxxxxx.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/52.0.2743.116 Safari/537.36"
    }


    def start_requests(self):
        for i in range(1, 50):  # 页数
            data = {'currentPage': str(i), 'recordCount': '505'}
            yield scrapy.FormRequest("http://www.ks.gov.cn/result?bureauId=41&status=1?currentPage=1&readCount=505",
                                    formdata=data, callback=self.parse)
            yield scrapy.FormRequest("http://www.ks.gov.cn/result?bureauId=43&status=1?currentPage=1&readCount=505",
                                     formdata=data,callback=self.parse)
        for j in range(1, 50):
            data = {'currentPage': str(j), 'recordCount': '1310'}
            yield scrapy.FormRequest('http://www.ks.gov.cn/result?bureauId=484',
                                     formdata=data,callback=self.parse)  # 改成post请求

    def parse(self, response):
        for i in range(0, 15):
            back_url = response.xpath('//*[@id="listForm"]/div[3]/ul/li/a/@href').extract()[i]
         #    url = self.baseurl + back_url
         #    yield Request(url, callback=self.get_content)
         # back_url = response.xpath('//*[@id="listForm"]/div[3]/ul/li/a/@href').extract()[0]
            url_content = back_url[0:6] + 'contentc' + back_url[-9:]
            url = self.baseurl + back_url
            url2 = self.baseurl + url_content
         # print(url_content)
            yield Request(url2, callback=self.get_content, meta={'url':url})

    def get_content(self, response):
        # print(response.text)
        # # overview = response.xpath('//*[@id="iframe"]').extarct()[0][0:40]
        content_pre = response.xpath('/html/body').xpath('string(.)').extract()
        content = str(content_pre).replace('/', '')
        # print(content)
        yield Request(response.meta['url'], callback=self.get_all, meta={'content': content})
        #
        # yield item

    def get_all(self, response):
        item = PolicyItem()
        department = response.xpath('//*[@class="MPT-table"]/tr[2]/td[2]').xpath('string(.)').extract()[0]
        date = response.xpath('//*[@class="MPT-table"]/tr[2]/td[4]').xpath('string(.)').extract()[0]
        name = response.xpath('//*[@class="MPT-table"]/tr[3]/td[2]').xpath('string(.)').extract()[0]
        item['content'] = response.meta['content']
        item['department'] = str(department).replace('/', '')
        item['date'] = str(date).replace('/', '')
        item['name'] = str(name).replace('/', '')
        item['overview'] = response.meta['content'][0:300]

        yield item