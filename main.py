import re

from bs4 import BeautifulSoup
from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse, JSONResponse

import httpx
import uvicorn

from components.structures import Urlentrance, Response_of_Parsing
from components.tools import get_html

app = FastAPI(debug=True)


@app.get("/", include_in_schema=False)
def root_docs():
    return RedirectResponse("/docs")


@app.get("/url_parsing/")
async def parsing_url_data(
        url_enter: Urlentrance = Query(..., description="Enter ur url for parsing")) -> Response_of_Parsing:
    data = await get_html(str(url_enter.url))

    soup = BeautifulSoup(data, 'html.parser')

    title_of_parsing = soup.title.text

    urls_of_parsing = [link.get('href') for link in soup.find_all('a')]

    return Response_of_Parsing(title=title_of_parsing, urls=urls_of_parsing)


@app.get("/parsing_again/")
async def parsing_wiki(url_enter: Urlentrance = Query(..., description="Enter ur url for parsing")):
    data = await get_html(str(url_enter.url))

    soup = BeautifulSoup(data, 'html.parser')

    info_table = soup.find("table", class_="infobox")

    paradigm = info_table.find("th", text='Парадигма')
    paradigm_data = paradigm.next_sibling.text

    creators = info_table.find("th", text='Творці')
    creators_data = creators.next_sibling.text

    developers = info_table.find("th", text='Розробник')
    developers_data = developers.next_sibling.text

    last_update = info_table.find("th", text=re.compile("Останній\s*реліз"))
    last_update_data = last_update.next_sibling.text

    return {
        "paradigm": paradigm_data,
        "creators": creators_data,
        "developers": developers_data,
        "last_update": last_update_data,

    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
