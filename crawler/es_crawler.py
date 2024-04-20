import re
from urllib.parse import urljoin

from data.db_orm.query_obj import create_reading_session
from data.db_orm.tables import TblHouses
from data.repository.house_repository import HouseRepository
from turbocrawler import CrawlerRequest, CrawlerResponse, ExtractRule
from turbocrawler.engine.control import StopCrawler
from turbocrawler.engine.url_extractor import UrlExtractor
from crawler.distritos import PROVINCIAS_ESPANHA

from crawler.credentials import HEADERS, COOKIES
from crawler.parsers.idealista_parser import house_parser
from crawler.idealista_crawler import IdealistaCrawler
from parsel import Selector


class IdealistaESCrawler(IdealistaCrawler):
    crawler_name = "IdealistaESCrawler"
    allowed_domains = ['idealista.com', 'www.idealista.com']
    time_between_requests = 1

    regex_extract_rules = [
        # ExtractRule(r'https://www.idealista.com/alquiler-viviendas/[a-z-]+-provincia/pagina-[0-9]+',remove_crawled=True),
        ExtractRule(r'https://www.idealista.com/alquiler-viviendas/[a-z-]+/pagina-[0-9]+', remove_crawled=True),
        # ExtractRule(r'https://www.idealista.com/inmueble/[0-9]+')
    ]
    country = "ES"

    def crawler_first_request(self) -> CrawlerResponse | None:
        for provincia in PROVINCIAS_ESPANHA:
            url = f'https://www.idealista.com/alquiler-viviendas/{provincia}/pagina-1.htm'
            district = provincia.replace("-provincia", "").upper()
            crawler_request = CrawlerRequest(url=url, kwargs={"district": district})
            self.crawler_queue.add(crawler_request=crawler_request)

        return None

    def process_request(self, crawler_request: CrawlerRequest) -> CrawlerResponse:
        response = self.session.get(crawler_request.url, headers=HEADERS, cookies=COOKIES)
        if response.status_code != 200:
            raise StopCrawler("response.status_code != 200")
        return CrawlerResponse(url=response.url,
                               body=response.text,
                               status_code=response.status_code,
                               kwargs={"district": crawler_request.kwargs["district"]})

    def process_response(self, crawler_request: CrawlerRequest, crawler_response: CrawlerResponse) -> None:
        if "https://www.idealista.com/alquiler-viviendas/" in crawler_response.url:

            # Disabling automatic_schedule to insert manually the urls
            crawler_response.settings.automatic_schedule = False
            crawler_response.settings.parse_response = False

            site_current_domain = UrlExtractor.get_url_domain(crawler_response.url)

            houses_to_scrape: list[str] = []
            houses_to_rescrape: list[str] = []
            houses_to_update: list[str] = []

            selector = Selector(crawler_response.body)
            houses_ele = selector.css("article[data-element-id]")

            site_houses = dict()
            for house in houses_ele:
                house_href = house.css('[class="item-link "]').attrib['href']
                house_url = urljoin(site_current_domain, house_href)

                price = house.css('[class="item-price h2-simulated"]::text').get()
                price = price.replace('.', '')
                price = int(price)

                site_houses[house_url] = {"price": price}

            houses_db = HouseRepository.get_houses_with_urls(site_houses.keys())
            for site_house_url, site_house_values in site_houses.items():
                match_house_db = None
                for house_db in houses_db:
                    if house_db.url == site_house_url:
                        match_house_db = house_db
                        break

                if match_house_db:
                    if match_house_db.price == site_house_values['price']:
                        houses_to_update.append(site_house_url)
                    else:
                        houses_to_rescrape.append(site_house_url)
                else:
                    houses_to_scrape.append(site_house_url)

            if houses_to_update:
                HouseRepository.update_houses_updated_at_with_urls(houses_to_update)

            for house_to_scrape in houses_to_scrape:
                crawler_request = CrawlerRequest(url=house_to_scrape, kwargs=crawler_request.kwargs)
                self.crawler_queue.add(crawler_request=crawler_request)

            for house_to_scrape in houses_to_rescrape:
                kwargs = {
                    **crawler_request.kwargs,
                    "update_house": True
                }
                crawler_request = CrawlerRequest(url=house_to_scrape, kwargs=kwargs)
                self.crawler_queue.add(crawler_request=crawler_request)

    def parse(self, crawler_request: CrawlerRequest, crawler_response: CrawlerResponse) -> None:
        if 'inmueble' in crawler_response.url:
            house_parser(crawler_request, crawler_response, self.country)
