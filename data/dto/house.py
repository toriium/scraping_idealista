from pydantic import BaseModel


class HouseDTO(BaseModel):
    site: str
    title: str
    price: int
    description: str | None
    kitchen: bool | None
    furnished: bool | None
    district: str
    address: str
    url: str
