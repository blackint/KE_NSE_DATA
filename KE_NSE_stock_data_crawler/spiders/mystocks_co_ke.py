import scrapy
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse as dateutil_parser
from bson import json_util
import json

from os import path
import os


class MystocksCoKeSpider(scrapy.Spider):
    PRICE_LIST_URL = "http://live.mystocks.co.ke/price_list/"
    name = "mystocks.co.ke"
    data_directory = "stock_data"
    allowed_domains = ["live.mystocks.co.ke"]
    start_urls = ["http://live.mystocks.co.ke/"]

    def url_generator(self):
        today = datetime.today().date()
        a_week_ago = today - timedelta(days=30)
        current_date = a_week_ago
        while current_date <= today:
            # Skip weekends
            if current_date.weekday() > 5 or path.exists(
                f"./{self.data_directory}/{current_date.isoformat()}.json"
            ):
                current_date = current_date + timedelta(days=1)
                continue

            yield f"{self.PRICE_LIST_URL}/{current_date.year}{current_date.month:02}{current_date.day:02}"
            current_date = current_date + timedelta(days=1)

    def price_list_gen(self, response):
        price_list_table_rows = response.css("table#pricelist").css("tr")
        for row in price_list_table_rows:
            yield row

    def get_float_cell_data(self, row_data, index, selector):
        cell_text = row_data[index].css(selector).get()
        try:
            value = float(cell_text.replace(",", ""))
        except ValueError:
            value = None

        return value

    def get_date(self, response):
        date_text = response.css("div#main").css("h2::text").get().split("for")[1]
        date = dateutil_parser(date_text).date()
        return date

    def file_writer(self, daily_price_data, isodate):
        with open(
            f"{os.getcwd()}/{self.data_directory}/{isodate}.json", "w", newline=""
        ) as jsonfile:
            self.logger.info(f"Writing data for day {isodate}")
            json.dump(daily_price_data, jsonfile, default=json_util.default)

    def start_requests(self):
        urls_gen = self.url_generator()
        for url in urls_gen:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        isodate = self.get_date(response).isoformat()
        row_iter = self.price_list_gen(response)

        data = []
        category = None
        for row in row_iter:
            row_data = row.css("td")
            category_text = row_data.css("td").css("h3::text").get()
            if category_text is not None:
                category = category_text
                continue

            try:
                # Check for symbol
                symbol = row_data[0].css("::text").get()
            except IndexError:
                # If we can't get symbol skip the row
                continue

            symbol = symbol.strip()
            symbol = symbol.strip("\n")
            # If there is no symbol skip the row
            if symbol is None or symbol == "":
                continue

            try:
                price_data = {
                    "symbol": symbol,
                    "category": category,
                    "date": isodate,
                    "name": row_data[1].css("a::text").get(),
                    "last_12_months": {
                        "low": self.get_float_cell_data(row_data, 2, "::text"),
                        "high": self.get_float_cell_data(row_data, 3, "::text"),
                    },
                    "days_trading": {
                        "low": self.get_float_cell_data(row_data, 4, "::text"),
                        "high": self.get_float_cell_data(row_data, 5, "::text"),
                        "price": self.get_float_cell_data(row_data, 6, "::text"),
                        "previous": self.get_float_cell_data(row_data, 7, "::text"),
                        "volume": self.get_float_cell_data(row_data, 11, "::text"),
                    },
                }
                data.append(price_data)
            except (IndexError, ValueError) as e:
                # Ignore irrelevant rows
                self.logger.error("error getting data for row", row_data.get(), e)
                continue

        try:

            self.file_writer(data, isodate)
        except FileNotFoundError:
            print(os.getcwd())
            import pdb

            pdb.set_trace()
