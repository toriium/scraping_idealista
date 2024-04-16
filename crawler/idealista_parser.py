from datetime import datetime

from parsel import Selector
from turbocrawler import CrawlerResponse

from data.dto.house import HouseDTO
from data.repository.house_repository import HouseRepository


def transform_price(price: str):
    return price.replace('.', '')


def get_kitchen_and_furnished(text) -> tuple[bool | None, bool | None]:
    if 'Mobilado e cozinha equipada' in text:
        kitchen = True
        furnished = True
    elif 'Cozinha equipada e casa sem mobília' in text:
        kitchen = True
        furnished = False
    elif 'Cozinha não equipada e casa sem mobília' in text:
        kitchen = False
        furnished = False
    else:
        kitchen = None
        furnished = None
    return kitchen, furnished


def get_district(location_list: list[str]):
    return location_list[-1].strip().split(',')[-1].strip()


def get_description(selector: Selector) -> str:
    description_list = selector.css('.adCommentsLanguage>p::text').getall()
    full_description = ""
    for description in description_list:
        full_description += f"{description.strip()}\n"
    return full_description


def house_parser(crawler_response: CrawlerResponse):
    if HouseRepository.get_house_by_url(url=crawler_response.url):
        return

    selector = Selector(crawler_response.body)

    deactivated_announce = selector.css('[class="deactivated-detail_container"]').get()
    if deactivated_announce:
        return

    house_to_buy = selector.css('[class="applyMortgageContainer "]').get()
    if house_to_buy:
        return

    title = selector.css('.main-info__title-main::text').get()

    price = selector.css('.info-data-price>span::text').get()
    price = transform_price(price=price)

    description = get_description(selector=selector)
    kitchen, furnished = get_kitchen_and_furnished(crawler_response.body)

    location_list = selector.css('.header-map-list::text').getall()
    district = get_district(location_list)
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
