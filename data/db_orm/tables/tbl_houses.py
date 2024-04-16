from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean, func
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
    country = Column(String(100), nullable=False, index=True)
    district = Column(String(100), nullable=False, index=True)
    address = Column(String(500), nullable=False)
    url = Column(Text(), nullable=False)
    updated_at = Column(DateTime(), nullable=False, server_default=func.now())



