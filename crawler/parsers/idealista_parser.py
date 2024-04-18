from datetime import datetime

from parsel import Selector

from crawler.parsers.abs_parser import ABCParser
from crawler.parsers.es_parser import IdealistaESParser
from crawler.parsers.pt_parser import IdealistaPTParser
from turbocrawler import CrawlerResponse

from data.dto.house import HouseDTO
from data.repository.house_repository import HouseRepository


def get_parser(country: str, selector) -> ABCParser:
    if country == "PT":
        return IdealistaPTParser(selector)

    if country == "ES":
        return IdealistaESParser(selector)


def house_parser(crawler_response: CrawlerResponse, country: str):
    if HouseRepository.get_house_by_url(url=crawler_response.url):
        return

    selector = Selector(crawler_response.body)
    parser = get_parser(country=country, selector=selector)

    deactivated_announce = selector.css('[class="deactivated-detail_container"]').get()
    if deactivated_announce:
        return

    house_to_buy = selector.css('[class="applyMortgageContainer "]').get()
    if house_to_buy:
        return

    title = selector.css('.main-info__title-main::text').get()

    price = selector.css('.info-data-price>span::text').get()
    price = parser.transform_price(price=price)

    rooms = parser.get_rooms()
    square_meters = parser.get_square_meters()

    description = parser.get_description()
    kitchen, furnished = parser.get_kitchen_and_furnished(crawler_response.body)

    location_list = selector.css('.header-map-list::text').getall()
    district = crawler_response.kwargs.get("district")
    address = ''
    for location in location_list:
        location = location.strip()
        if address:
            address = f'{address}, {location}'
        else:
            address = f'{location}'

    data = {
        "site": 'idealista',
        "title": title,
        "price": price,
        "rooms": rooms,
        "square_meters": square_meters,
        "description": description,
        "kitchen": kitchen,
        "furnished": furnished,
        "country": country,
        "district": district,
        "address": address,
        "url": crawler_response.url,
        "updated_at": datetime.now(),
    }
    house = HouseDTO(**data)
    HouseRepository.insert_house(house)
