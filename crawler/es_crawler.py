from turbocrawler import CrawlerRequest, CrawlerResponse, ExtractRule
from turbocrawler.engine.control import StopCrawler

from crawler.distritos import PROVINCIAS_ESPANHA

from crawler.credentials import HEADERS, COOKIES
from crawler.parsers.idealista_parser import house_parser
from crawler.idealista_crawler import IdealistaCrawler


class IdealistaESCrawler(IdealistaCrawler):
    crawler_name = "IdealistaESCrawler"
    allowed_domains = ['idealista.com', 'www.idealista.com']
    regex_extract_rules = [
        ExtractRule(r'https://www.idealista.com/alquiler-viviendas/[a-z-]+-provincia/pagina-[0-9]+',remove_crawled=True),
        ExtractRule(r'https://www.idealista.com/alquiler-viviendas/[a-z-]+/pagina-[0-9]+',remove_crawled=True),
        ExtractRule(r'https://www.idealista.com/inmueble/[0-9]+')
    ]
    time_between_requests = 2
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

    def parse(self, crawler_request: CrawlerRequest, crawler_response: CrawlerResponse) -> None:
        if 'inmueble' in crawler_response.url:
            house_parser(crawler_response, self.country)
