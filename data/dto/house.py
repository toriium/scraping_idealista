from datetime import datetime

from pydantic import BaseModel


class HouseDTO(BaseModel):
    site: str
    title: str
    price: int
    rooms: int
    square_meters: int
    description: str | None
    kitchen: bool | None
    furnished: bool | None
    country: str
    district: str
    address: str
    url: str
    created_at: datetime
    updated_at: datetime
