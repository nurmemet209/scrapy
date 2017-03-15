import scrapy
import pymysql
import urllib

from tutorial.items import CrarBrandItem

english_name_list = []
car_brand_list = []


class BaiKeSpider(scrapy.Spider):
    name = "baike"
    start_urls = []

    def __init__(self):
        self.start_urls = []
        set_url(self.start_urls)

    def closed(spider, reason):
        for item in english_name_list:
            print(item)
        update_db(english_name_list)

    def parse(self, response):
        item = CrarBrandItem()
        # response.xpath("/html/body/div[3]/div[2]/div/div[2]/div[4]/div[1]/a[1]/text()").extract()
        data_ = response.xpath("//*[@id=1]/h3/a[1]/text()").extract()
        english_name_list.append({'zh_name': urllib.parse.unquote(get_zh_name(response.url)), 'en_name': data_})
        # if len(data_) is not 0:
        #     data=data_[0]
        #     sindex=data.find('（')
        #     eindex=data.find('）')
        #     if sindex!=-1 and eindex!=-1:
        #         m=data[sindex+1:eindex]
        #         aindex=m.find('</a>')
        #         zh_name_index_s=response.url.find('item/')
        #         zh_name_index_e=response.url.find('?')
        #         zh_name=response.url[zh_name_index_s+5:zh_name_index_e]
        #         if aindex!=-1:
        #             c=response.xpath("/html/body/div[3]/div[2]/div/div[2]/div[4]/div[1]/a[1]/text()").extract()
        #             item['en_name'] = c
        #             english_name_list.append({'zh_name': urllib.parse.unquote(zh_name), 'en_name': c[0]})
        #         else:
        #             item['en_name']=m
        #             english_name_list.append({'zh_name': urllib.parse.unquote(zh_name), 'en_name': m})


        yield item


def get_zh_name(url):
    zh_name_index_s = url.find('wd=')
    zh_name=url[zh_name_index_s+1:]
    return zh_name


def set_url(urls):
    car_brand_list = getCarBrandList()
    for item in car_brand_list:
        # urls.append("http://baike.baidu.com/item/斯巴鲁?sefr=sebtn")
        urls.append("https://www.baidu.com/s?wd=" + item[1])
        return


devdatabasename = "pppcar-supplier-dev"
prodatabasename = "pppcar-supplier"
devUrl = "rm-bp167v39m44a2ygxqo.mysql.rds.aliyuncs.com"
devUserName = "pppcar_dev"
devPassward = "pppcar2015Remuszpj"


def getCarBrandList():
    database_name = "mtva-dev"
    db = pymysql.connect(devUrl, devUserName, devPassward, database_name, charset="utf8")
    cursor = db.cursor()
    sql = "select id,brand_name from bs_car_brand"
    cursor.execute(sql)
    car_brand_name_list = cursor.fetchall()
    db.close()
    return car_brand_name_list


def update_db(en_name_list):
    database_name = "mtva-dev"
    db = pymysql.connect(devUrl, devUserName, devPassward, database_name, charset="utf8")
    cursor = db.cursor()
    for item in en_name_list:
        update(db, cursor, item['zh_name'], item['en_name'])


def update(db, cursor, brand_name, english_name):
    update_sql = "update bs_car_brand set english_name = '%s' where brand_name = '%s'" % (english_name, brand_name)
    print(update_sql)
    try:
        cursor.execute(update_sql)
        db.commit()
        print("成功")
    except:
        print("失败")
        db.rollback()
