from pydantic import HttpUrl, BaseModel

class Urlentrance(BaseModel):
    url: HttpUrl


class Response_of_Parsing(BaseModel):
    title: str = ""
    urls: list[str | None] = []
