from typing import Literal

import requests
from turbocrawler import Crawler, CrawlerRequest, CrawlerResponse, ExecutionInfo
from turbocrawler.engine.control import StopCrawler

from crawler.distritos import DISTRITOS_PORTUGAL

from crawler.credentials import HEADERS, COOKIES
from crawler.parsers.idealista_parser import house_parser
from data.db_orm.query_obj import create_reading_session


class IdealistaCrawler(Crawler):
    time_between_requests = 1

    session: requests.Session

    country: Literal["ES", "PT"]

    def start_crawler(self) -> None:
        self.session = requests.session()

    def crawler_first_request(self) -> CrawlerResponse | None:
        for distrito in DISTRITOS_PORTUGAL:
            url = f'https://www.idealista.pt/arrendar-casas/{distrito}-distrito/pagina-1'
            crawler_request = CrawlerRequest(url=url)
            self.crawler_queue.add(crawler_request=crawler_request)

        return None

    def process_request(self, crawler_request: CrawlerRequest) -> CrawlerResponse:
        response = self.session.get(crawler_request.url, headers=HEADERS, cookies=COOKIES)
        if response.status_code != 200:
            raise StopCrawler("response.status_code != 200")
        return CrawlerResponse(url=response.url,
                               body=response.text,
                               status_code=response.status_code)

    def stop_crawler(self, execution_info: ExecutionInfo) -> None:
        self.session.close()
