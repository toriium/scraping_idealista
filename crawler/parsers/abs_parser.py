from abc import ABC, abstractmethod

from parsel import Selector


class ABCParser(ABC):

    def __init__(self, selector: Selector):
        self.selector = selector

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
