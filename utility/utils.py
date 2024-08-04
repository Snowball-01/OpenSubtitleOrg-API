import aiohttp
from bs4 import BeautifulSoup
from typing import List


async def fetch_server_location():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://ipinfo.io/json") as response:
                data = await response.json()
                return f"{data['city']}, {data['region']}, {data['country']}"
    except Exception as e:
        return "Location unknown"

async def fetch_subtitles(url: str) -> List[dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            soup = BeautifulSoup(text, "lxml")
            data = []

            for el in soup.find_all("tr", onclick=True):
                td_elements = el.find_all("td")

                br_element = td_elements[0].find("br")
                br_text = br_element.next_sibling.text.strip() if br_element else "None"
                span_text = td_elements[0].find("span").text.strip() if td_elements[0].find("span") else ""

                lang = td_elements[1].find("a")["title"] if len(td_elements) > 1 else "Unknown"
                imdb = td_elements[7].find("a").text if len(td_elements) >= 7 else "None"

                raw_title = el.find("a").text.strip()
                clean_title = raw_title.replace("\n", "").replace("\\", "").replace('"', "")

                subtitle = {
                    "id": el.find("a")["href"].split("/")[3],
                    "title": clean_title,
                    "description": br_text + span_text,
                    "lang": lang,
                    "sub_type": td_elements[4].find("span").text,
                    "imdb": f"{imdb}/10",
                    "url": f'https://www.opensubtitles.org{el.find("a")["href"]}',
                    "download": f"https://www.opensubtitles.org/en/subtitleserve/sub/{el.find('a')['href'].split('/')[3]}",
                }
                data.append(subtitle)

            if not data:
                object = {
                    "id": url.split("/")[-1],
                    "title": soup.find("span", attrs={"itemprop": "name"}).text.strip(),
                    "description": soup.find("h2").text.strip(),
                    "lang": soup.find("span", attrs={"itemprop": "name"}).text.strip().split(" ")[-1],
                    "sub_type": soup.find("h2").text.strip().split(" ")[-1],
                    "imdb": soup.find("span", attrs={"itemprop": "ratingValue"}).text.strip() + "/" + "10",
                    "url": url,
                    "download": soup.find("a", attrs={"title": "Download"})["href"],
                }
                data.append(object)
            
            return data

async def fetch_query(query: str) -> List[dict]:
    url = f"https://www.opensubtitles.org/en/search2/sublanguageid-all/moviename-{query.replace(' ', '+')}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            soup = BeautifulSoup(text, "lxml")
            data = []

            for el in soup.find_all("tr", onclick=True):
                raw_title = el.find("a").text.strip()
                clean_title = raw_title.replace("\n", "").replace("\\", "").replace('"', "")

                description_span = el.find("span", attrs={"class": "p"})
                description = "".join(description_span.stripped_strings) if description_span else ""

                query_result = {
                    "id": el.get("onclick").split("/")[-1].replace("')", ""),
                    "title": clean_title,
                    "description": description,
                    "image": f"https://{el.find('img')['src'][2:]}",
                    "imdb": f'{el.find("td", attrs={"align": "center"}).text}/10',
                    "url": f'https://www.opensubtitles.org{el.find("a")["href"]}',
                    "download": f"https://www.opensubtitles.org/en/subtitleserve/sub/{el.find('a')['href'].split('/')[3]}",
                }
                data.append(query_result)

            return data
