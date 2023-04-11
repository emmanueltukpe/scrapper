from scrapy import *


class Accommodation(Spider):
    
    name = "finelib"
    start_urls = ["https://www.finelib.com/"]
    
    def join_lists_to_dict(self, list_a, list_b):
        if len(list_a) != 0 and len(list_b) != 0:
            my_dict = dict(zip(list_a, list_b))
            return my_dict
        else:
            return {}

    def parse(self, response):
        links = response.css(
            'div.city-list > ul > li > a::attr(href)').extract()
        links = [f"https://www.finelib.com{link}" for link in links if link.startswith("/")]
        for link in links:
            yield Request(url=link, callback=self.parse_links)
            # yield {"link": link}

    def parse_links(self, response):
        links = response.css("div.city-list-inner.city-list-col > ul > li > a::attr(href)").extract()
        links = [f"https://www.finelib.com{link}" for link in links if link.startswith("/")]
        for link in links:
            yield Request(url=link, callback=self.parse_pages)

    def parse_pages(self, response):
        # self.business = response.css("div.middle-curve > h1::text").extract_first()
        links = response.css("div.category-list.newlist > ul > li > a::attr(href)").extract()
        links = [f"https://www.finelib.com{link}" for link in links if link.startswith("/")]
        more_info =  response.css("div.cmpny-lstng.url > a::attr(href)").extract()
        for info in more_info:
            yield Request(url=info, callback=self.parse_hyperlinks)
            
        next_page = response.css('div.paging-box a:last-child::attr(href)').extract_first()
        if next_page is not None:
            if next_page.startswith('/'):
                next_page = f"https://www.finelib.com{next_page}"
                yield Request(url=next_page, callback=self.parse_pages)
            else:
                yield Request(url=next_page, callback=self.parse_pages)
        if links is not []:
            for link in links:
                yield Request(url=link, callback=self.parse_pages)
            # body > div.container > div.middle-curve > div > a:nth-child(3)
    def parse_hyperlinks(self, response):
        business = response.css("div.breadcrumb > a:nth-child(3)::text").extract_first()
        city = response.css("div.breadcrumb > a:nth-child(2)::text").extract_first()
        categories = response.css("div.breadcrumb > a::text").extract()
        categories = categories[3:]
        name = response.css(
            "div.box-headings.box-new-hed > h1 > span::text").extract()
        address = response.css("div.cmpny-lstng-1 > span::text").extract()
        phonenumber = response.css(
            "div.cmpny-lstng-1 > span > a::text").extract()
        url = response.css(
            "div.tel-no-div > div.cmpny-lstng.url > a::text").extract()
        url = url[0] if url != [] else ""
        headings = response.css("div.subb-bx.MT-15 > h3::text").extract()
        removing = ["Short Description", "E-mail Contact"]
        short_description = response.css(
            "div.subb-bx.MT-15 > p > span::text").extract()
        email_contact = response.css(
            "div.subb-bx.MT-15 > p > a::text").extract()
        email_contact = "" if email_contact == [] else email_contact[0]
        paragraphs = response.css("div.subb-bx.MT-15 > p::text").extract()
        if removing[0] in headings:
            headings.remove(removing[0])
        if removing[1] in headings:
            headings.remove(removing[1])
        other_info = self.join_lists_to_dict(headings, paragraphs)
        unsorted_obj = {
            # "data": self.data,
            "name": name[0],
            "address": ",".join(address),
            "phonenumber": phonenumber,
            "email_contact": email_contact,
            "url": url,
            "short_description": short_description[0],
        }
        dictt = {**unsorted_obj, **other_info}
        
        if categories != []:
            cat_dict = {}
            current_dict = cat_dict
            for e in categories[:-1]:
                current_dict[e] = {}
                current_dict = current_dict[e]
            current_dict[categories[-1]] = dictt
            res = {city: {business: cat_dict}}
            yield res
        else:
            res = {city: {business: dictt}}
            yield res
