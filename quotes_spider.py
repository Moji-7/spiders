
import scrapy
from scrapy import Selector
import json
from types import SimpleNamespace
import mysql_connection as mydb
from python_mysql_dbconfig import read_db_config
from mysql.connector import MySQLConnection, Error
import operations as digi, digiItem as digiItems
import scrapy
from scrapy import Selector
import json
import time  
from types import SimpleNamespace
import mysql_connection as mydb
from python_mysql_dbconfig import read_db_config
from mysql.connector import MySQLConnection, Error
import operations as digi, digiItem as digiItems

class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        urls = [
         'https://www.digikala.com/search/category-men-tee-shirts-and-polos/?pageno=2&sortby=26']
        for url in urls:
            yield scrapy.Request(url=url, callback=(self.parse))

    def parse(self, response):
        digiItems = []
        products = response.css('.c-listing__items.js-plp-products-list').xpath('li').getall()
        for product in products:
            sel = Selector(text=product)
            digiInfo = self.getBaseInfo(sel)
            otherInfo = self.getOtherInfo(sel)
            sellerInfo = self.getSellerInfo(sel)
            decisionInfo = self.calcDecisionInfo(sel)
            digiInfo.product_url = otherInfo[0]
            digiInfo.img = otherInfo[1]
            digiInfo.getdate = otherInfo[2]
            
            digiItems.append(vars(digiInfo))
            print(product)

        insert_item(digiItems)
        page = response.url.split('/')[(-2)]
        filename = f"quotes-{page}.html"
        with open(filename, 'wb') as (f):
            f.write(''.join(products).encode())
        self.log(f"Saved file {filename}")

    def getOtherInfo(self, sel):
        returns = dict()
        aTag = sel.css('.js-product-item.js-product-url::attr(data-snt-params)').extract()[0]
        returns['product_url'] = json.loads(aTag, object_hook=(lambda d: SimpleNamespace(**d))).product_url
        returns['imgsrc'] = sel.css('.js-product-item.js-product-url img::attr(src)').extract()[0]
        returns['getdate'] =  time.strftime('%Y-%m-%d %H:%M:%S')
        return list(returns.values())

    def getBaseInfo(self, sel):
        objInfo = sel.css('.c-product-box::attr(data-enhanced-ecommerce)').get()
        digiInfo = json.loads(objInfo, object_hook=(lambda d: SimpleNamespace(**d)))
        digiInfo.oldPrice = sel.css('.c-price__value del::text').get()
        digiInfo.discount = '70'
        return digiInfo
    
    
    def getSellerInfo(self, sel):
        hasManySeller?;
        return digiInfo

    def calcDecisionInfo(self, sel):
        maxPrice=?
        minPrice=?
        diffPrice=?
        retainsCount=?
        return digiInfo
         

def insert_item(items):
 
    try:
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            cursor.executemany('\n    INSERT INTO item(digiId,name,category,brand,variant,price,quantity,oldPrice,discount,product_url,img,getdate)\n    VALUES (%(id)s, %(name)s, %(category)s, %(brand)s, %(variant)s, %(price)s, %(quantity)s, %(oldPrice)s, %(discount)s, %(product_url)s, %(img)s, %(getdate)s)', items)
            conn.commit()
        except Error as e:
            try:
                print('Error:', e)
            finally:
                e = None
                del e

    finally:
        cursor.close()
        conn.close()
# okay decompiling quotes_spider.cpython-37.pyc