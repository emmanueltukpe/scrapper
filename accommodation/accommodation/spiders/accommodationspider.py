from scrapy import *


class Accommodation(Spider):
    name = "finelib"
    start_urls = ["https://www.finelib.com/"]

    def parse(self, response):
        links = response.css(
            'div.category-list > ul > li > a::attr(href)').extract()
        links = [link.replace('//', 'https://') for link in links]
        for link in links:
            yield Request(url=link, callback=self.parse_links)

    def parse_links(self, response):
        links = response.css("div.cmpny-lstng.url > a::attr(href)").extract()

        for link in links:
            yield Request(url=link, callback=self.parse_pages)

    def parse_pages(self, response):
        name = response.css(
            "div.box-headings.box-new-hed > h1::text").extract()
        address = response.css("div.cmpny-lstng-1::text").extract()
        phonenumber = response.css("div.cmpny-lstng-1 > a::text").extract()
        email = response.css(
            "div.tel-no-div > div.cmpny-lstng.url > a::text").extract()
        try:
            unsorted_obj = {
                "name": name[0],
                "address": address[0],
                "phonenumber": phonenumber,
                "email": email[0]
            }
            yield unsorted_obj
        except:
            unsorted_obj = {
                "name": name[0],
                "address": address[0],
                "phonenumber": phonenumber,
                "email": ""
            }
            yield unsorted_obj
