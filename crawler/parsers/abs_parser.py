from abc import ABC, abstractmethod

from parsel import Selector


class ABCParser(ABC):

    def __init__(self, selector: Selector):
        self.selector = selector

    @staticmethod
    def get_only_numbers(text: str) -> str:
        ints = [char for char in text if char.isnumeric()]
        return "".join(ints)

    @staticmethod
    def transform_price(price: str):
        return price.replace('.', '')

    @staticmethod
    def get_district(location_list: list[str]):
        return location_list[-1].strip().split(',')[-1].strip()

    def get_description(self) -> str:
        description_list = self.selector.css('.adCommentsLanguage>p::text').getall()
        full_description = ""
        for description in description_list:
            full_description += f"{description.strip()}\n"
        return full_description

    @staticmethod
    @abstractmethod
    def get_kitchen_and_furnished(text) -> tuple[bool | None, bool | None]:
        ...

    def get_rooms(self) -> int:
        value = self.selector.css("div.info-features > span:nth-child(2)::text").get()
        rooms = int(self.get_only_numbers(value))
        return rooms

    def get_square_meters(self) -> int:
        value = self.selector.css("div.info-features > span:nth-child(1)::text").get()
        square_meters = self.get_only_numbers(value)
        square_meters = square_meters.replace('²', '')
        return int(square_meters)
