import unittest
from datetime import datetime,timedelta
from KE_NSE_stock_data_crawler.spiders.mystocks_co_ke import MystocksCoKeSpider

import requests

class TestMystocksCoKeSpider(unittest.TestCase):

    def setUp(self):
        spider = MystocksCoKeSpider()
        self.url_gen = spider.url_generator()
        


    def test_url_generator__generates_valid_urls(self):
        for url in self.url_gen:
            self.assertTrue(url.startswith("http://live.mystocks.co.ke/price_list/"))
    
    def test_url_generator__valid_url_paths(self):
        one_week_ago = datetime.today()-timedelta(weeks=1)
        active_date = one_week_ago
        for url in self.url_gen:
            self.assertEqual(f"{MystocksCoKeSpider.PRICE_LIST_URL}{active_date.year}{active_date.month:02}{active_date.day:02}",url)
            active_date= active_date+timedelta(days=1) 


    def test_url_generator__respone_200(self):
        url = next(self.url_gen)
        response = requests.get(url)
        self.assertEqual(response.status_code,200)


            

      

if __name__ == '__main__':
    unittest.main()