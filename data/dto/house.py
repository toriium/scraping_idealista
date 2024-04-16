from datetime import datetime

from pydantic import BaseModel


class HouseDTO(BaseModel):
    site: str
    title: str
    price: int
    description: str | None
    kitchen: bool | None
    furnished: bool | None
    country: str
    district: str
    address: str
    url: str
    updated_at: datetime
