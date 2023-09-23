from sqlalchemy import Column, Date, Integer, String, Text, Boolean
from data.db_orm.tables.base import Base


class TblHouses(Base):
    __tablename__ = 'tbl_houses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    site = Column(String(100), nullable=False)
    title = Column(String(500), nullable=False)
    price = Column(Integer(), nullable=False)
    description = Column(Text(), nullable=True)
    kitchen = Column(Boolean(), nullable=True, index=True)
    furnished = Column(Boolean(), nullable=True, index=True)
    district = Column(String(100), nullable=False, index=True)
    address = Column(String(500), nullable=False)
    url = Column(Text(), nullable=False)



