import scrapy
from ..items import *
from math import radians, cos, sin, asin, sqrt

def haversine(lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """

    lon1 = 20.4600347
    lat1 = 44.8161635
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


class HappyScrapy(scrapy.Spider):
    name = "HappyScrapy"
    start_urls = [
        'https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/lista/po-stranici/20/',
        'https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/izdavanje/lista/po-stranici/20/',
        'https://www.nekretnine.rs/stambeni-objekti/kuce/izdavanje-prodaja/prodaja/lista/po-stranici/20/',
        'https://www.nekretnine.rs/stambeni-objekti/kuce/izdavanje-prodaja/izdavanje/lista/po-stranici/20/'
        # 'https://www.nekretnine.rs/stambeni-objekti/stanovi/stari-grad-dorcol-91m2/Nkzma6UHv08/',
        # 'https://www.nekretnine.rs/stambeni-objekti/stanovi/stari-grad-gundulicev-venac-svetozara-miletica-20-55m2-500-eur/NkGcPbi1YcO/'
    ]

    def parse(self, response):
        props_on_page = self.get_properties_on_page(response)
        for prop_page in props_on_page:
            yield response.follow(prop_page, callback=self.parse_prop)
        # yield response.follow(response.url, callback=self.parse_prop)

        next_page = response.css("a.next-article-button::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def get_properties_on_page(self, response):
        prop_links = [link.get() for link in response.css("h2 a::attr(href)")]
        return prop_links

    def get_location(self, response):
        # print()
        location_tag=response.css("div.property__location ul li")
        if len(location_tag)>2:
            location = location_tag[2].css("li::text").get()
        else:
            location = location_tag[1].css("li::text").get()
        if location=='Beograd':
            block = location_tag[3].css("li::text").get()
        else:
            block = None
        return location, block

    def get_text_from_list(self, tag, pat):
        for li in tag:
            if li.css("li::text").get().strip() == pat:
                return tag.index(li)+1

        return -1

    def get_text_from_list_span(self, tag, pat):
        for li in tag:
            if li.css("li span::text").extract()[0] == pat:
                return tag.index(li)

        return -1

    def get_details(self, response):
        details_tag = response.css(
            "section#detalji div.property__amenities")[0]

        add_type_index = self.get_text_from_list(details_tag.css("ul li"), "Transakcija:")
        add_type = details_tag.css("ul li:nth-child({}) strong::text".format(
            add_type_index)).get().strip() if add_type_index > -1 else None
        if add_type == 'Prodaja':
            add_type = 's'
        if add_type == 'Izdavanje':
            add_type = 'r'

        size_index = self.get_text_from_list(details_tag.css("ul li"), "Kvadratura:")
        size = float(details_tag.css("ul li:nth-child({}) strong::text".format(
            size_index)).get().strip().split(" ")[0]) if size_index > -1 else None

        area_index = self.get_text_from_list(details_tag.css("ul li"), "Površina zemljišta:")
        area = float(details_tag.css("ul li:nth-child({}) strong::text".format(
            area_index)).get().strip().split(" ")[0]) if area_index > -1 else None

        year_index = self.get_text_from_list(details_tag.css("ul li"), "Godina izgradnje:")
        year = int(details_tag.css("ul li:nth-child({}) strong::text".format(year_index)
                                   ).get().strip()) if year_index > -1 else None

        rooms_index = self.get_text_from_list(details_tag.css("ul li"), "Ukupan broj soba:")
        rooms = float(details_tag.css("ul li:nth-child({}) strong::text".format(
            rooms_index)).get().strip()) if rooms_index > -1 else None

        toiletes_index = self.get_text_from_list(details_tag.css("ul li"), "Broj kupatila:")
        toiletes = int(details_tag.css("ul li:nth-child({}) strong::text".format(
            toiletes_index)).get().strip()) if toiletes_index > -1 else None

        storey_index = self.get_text_from_list(details_tag.css("ul li"), "Spratnost:")
        storey = details_tag.css("ul li:nth-child({}) strong::text".format(
            storey_index)).get().strip() if storey_index > -1 else None
        if storey == 'Prizemlje' or storey == 'Visoko prizemlje':
            storey = 0
        if storey == 'Suteren':
            storey = -1
        if storey != None:
            storey = int(storey)

        total_storeys_index = self.get_text_from_list(
            details_tag.css("ul li"), "Ukupan broj spratova:")
        total_storeys = int(details_tag.css("ul li:nth-child({}) strong::text".format(
            total_storeys_index)).get().strip()) if total_storeys_index > -1 else None

        registered_index = self.get_text_from_list(details_tag.css("ul li"), "Uknjiženo:")

        if registered_index == -1:
            main_tag = response.css("div.property__main-details ul li")
            registered_index=self.get_text_from_list_span(main_tag, "Uknjiženo:")   
            # print(registered_index)   
            # print(main_tag[registered_index])   
            registered = main_tag[registered_index].css("li span::text").extract()[1] if registered_index > -1 else None
            if registered != None:
                registered = 1 if registered == 'Da' else 0
        else:
            registered = details_tag.css("ul li:nth-child({}) strong::text".format(
                registered_index)).get().strip() if registered_index > -1 else None
            if registered != None:
                registered = 1 if registered == 'Da' else 0
        return add_type, size, area, year, rooms, toiletes, storey, total_storeys, registered

    def get_price(self, response):
        price = response.css("h4.stickyBox__price::text").get()
        if len(price) > 1:
            price = price.split(" ")[:-2]
            price = ("").join(price)
            price = float(price)

        return price

    def get_heat_parking(self, response):
        main_tag = response.css("div.property__main-details ul li")
        heat = main_tag[2].css("li span::text").extract()[1]
        parking = main_tag[3].css("li span::text").extract()[1]
        parking = 1 if parking == 'Da' else 0
        return heat, parking

    def parse_prop(self, response):
        item = WebcrawlerItem()
        location, block = self.get_location(response)
        if location == 'Beograd':
            js=response.css("section#lokacija script::text").extract()[-1]
            lat_long=js.replace('\n','').replace(' ','').strip().split(",")
            lng=float(lat_long[1].split("=")[1])
            lat=float(lat_long[2].split("=")[1])
            distance_from_center = haversine(lng, lat)
        else:
            distance_from_center=None
        prop_type = 'a' if response.url.split("/")[-4] == 'stanovi' else 'h'
        add_type, size, area, year, rooms, toiletes, storey, total_storeys, registered = self.get_details(
            response)
        price = self.get_price(response)
        heat_type, parking = self.get_heat_parking(response)
        other = ''

        item["url"] = response.url
        item["property_type"] = prop_type
        item["location"] = location
        item["block"] = block
        item["distance_from_center"]=distance_from_center
        item["add_type"] = add_type
        item["size"] = size
        item["year"] = year
        item["rooms"] = rooms
        item["toiletes"] = toiletes
        item["storey"] = storey
        item["total_storeys"] = total_storeys
        item["registered"] = registered
        item["price"] = price
        item["other"] = other
        item["area"] = area
        item["heat_type"] = heat_type
        item["parking"] = parking

        # print(item)

        yield item
