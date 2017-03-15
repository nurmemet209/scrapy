import scrapy

from tutorial.items import HubItem


from selenium import webdriver


class HubSpider(scrapy.Spider):
    name = "jingdong"
    allowed_domains = ["jd.com"]
    start_urls = ["https://search.jd.com/Search?keyword=%E8%BD%AE%E6%AF%82&enc=utf-8&suggest=1.rem.0.T03&wq=%E8%BD%AE%E6%AF%82&pvid=b9h73hzi.79dfgvq4"]

    def parse(self, response):
        driver = webdriver.Chrome("D:\software\chromedriver_win32\chromedriver.exe",9515)
        test=driver.get(response.url)


        for sel in response.xpath('//ul/li'):
            item = HubItem()
            item['title'] = sel.xpath('//*[@id="J_goodsList"]/ul/li[1]/div/div[3]/a/@title').extract()
            item['link'] = sel.xpath('//*[@id="J_goodsList"]/ul/li[1]/div/div[1]/a/@href').extract()
            item['img' ] = sel.xpath('//*[@id="J_goodsList"]/ul/li[1]/div/div[1]/a/img/@src').extract()
            item['price'] = sel.xpath('//*[@id="J_goodsList"]/ul/li[1]/div/div[2]/strong/@data-price').extract()
            yield item
        next_page = response.css('li.next a::attr(href)').extract_first()
