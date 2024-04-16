from data.db_orm.query_obj import insert_obj, select_first_obj, select_all_obj
from data.db_orm.sql_error import SQLError
from data.db_orm.tables.tbl_houses import TblHouses
from data.dto.house import HouseDTO


class HouseRepository:
    @staticmethod
    def get_house_by_url(url):
        return select_first_obj(TblHouses, filter_by={"url": url})

    @staticmethod
    def get_all_houses_() -> list[TblHouses]:
        return select_all_obj(TblHouses, dict())

    @staticmethod
    def insert_house(house: HouseDTO) -> tuple[HouseDTO | None, SQLError | None]:
        new_house = TblHouses()
        new_house.site = house.site
        new_house.title = house.title
        new_house.price = house.price
        new_house.description = house.description
        new_house.kitchen = house.kitchen
        new_house.furnished = house.furnished
        new_house.country = house.country
        new_house.district = house.district
        new_house.address = house.address
        new_house.url = house.url

        query_result, error = insert_obj(obj=new_house)
        if error:
            if error == SQLError.duplicate_entry:
                return None, SQLError.duplicate_entry

        return house, None
