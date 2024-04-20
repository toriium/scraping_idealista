from data.db_orm.query_obj import insert_obj, update_obj, select_first_obj, select_all_obj, create_reading_session
from data.db_orm.sql_error import SQLError
from data.db_orm.tables.tbl_houses import TblHouses
from data.dto.house import HouseDTO
from sqlalchemy import update
from datetime import datetime
from sqlalchemy.dialects import mysql


class HouseRepository:

    @staticmethod
    def __create_house_obj(house: HouseDTO):
        new_house = TblHouses()
        new_house.site = house.site
        new_house.title = house.title
        new_house.price = house.price
        new_house.rooms = house.rooms
        new_house.square_meters = house.square_meters
        new_house.description = house.description
        new_house.kitchen = house.kitchen
        new_house.furnished = house.furnished
        new_house.country = house.country
        new_house.district = house.district
        new_house.address = house.address
        new_house.url = house.url
        new_house.created_at = house.created_at
        new_house.updated_at = house.updated_at
        return new_house

    @staticmethod
    def get_house_by_url(url):
        return select_first_obj(TblHouses, filter_by={"url": url})

    @staticmethod
    def get_all_houses_() -> list[TblHouses]:
        return select_all_obj(TblHouses, dict())

    @staticmethod
    def get_houses_with_urls(urls: list[str]):
        with create_reading_session() as session:
            return session.query(TblHouses).filter(TblHouses.url.in_(urls)).all()

    @staticmethod
    def update_houses_updated_at_with_urls(urls: list[str]):
        with create_reading_session() as session:
            stmt = (
                update(TblHouses)
                .where(TblHouses.url.in_(urls))
                .values(updated_at=datetime.today())
            )
            session.execute(stmt)
            session.commit()

    @classmethod
    def update_house(cls, house: HouseDTO) -> SQLError | None:
        house = cls.__create_house_obj(house)
        query_result, error = update_obj(obj_table=TblHouses,
                                         filter_by={"url": house.url},
                                         obj_update=house)

    @classmethod
    def insert_house(cls, house: HouseDTO) -> tuple[HouseDTO | None, SQLError | None]:
        house = cls.__create_house_obj(house)

        query_result, error = insert_obj(house)
        if error:
            if error == SQLError.duplicate_entry:
                return None, SQLError.duplicate_entry

        return house, None
