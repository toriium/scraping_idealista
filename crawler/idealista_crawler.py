from pprint import pprint

import requests
from parsel import Selector
from turbocrawler import Crawler, CrawlerRequest, CrawlerResponse, CrawlerRunner

from crawler.distritos import DISTRITOS_PORTUGAL

from crawler.credentials import HEADERS, COOKIES
from crawler.idealista_parser import house_parser


class IdealistaCrawler(Crawler):
    crawler_name = "IdealistaCrawler"
    allowed_domains = ['idealista.pt']
    regex_rules = [r'^/arrendar-casas/[a-z-]+-distrito/pagina-[0-9]+', r'^/imovel/[0-9]+']
    time_between_requests = 2

    session: requests.Session

    def start_crawler(self) -> None:
        self.session = requests.session()

    def crawler_first_request(self) -> CrawlerResponse | None:
        for distrito in DISTRITOS_PORTUGAL:
            url = f'https://www.idealista.pt/arrendar-casas/{distrito}-distrito/pagina-1'
            crawler_request = CrawlerRequest(site_url=url)
            self.crawler_queue.add_request_to_queue(crawler_request=crawler_request)

        url = "https://www.idealista.pt"
        response = self.session.get(url=url, headers=HEADERS, cookies=COOKIES)
        return None

    def process_request(self, crawler_request: CrawlerRequest) -> CrawlerResponse:
        response = self.session.get(crawler_request.site_url, headers=HEADERS, cookies=COOKIES)
        return CrawlerResponse(site_url=response.url,
                               site_body=response.text,
                               status_code=response.status_code)

    def parse_crawler_response(self, crawler_response: CrawlerResponse) -> None:
        if 'imovel' in crawler_response.site_url:
            house_parser(crawler_response)

    def stop_crawler(self) -> None:
        self.session.close()


CrawlerRunner(crawler=IdealistaCrawler).run()
