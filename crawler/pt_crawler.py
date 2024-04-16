from turbocrawler import CrawlerRequest, CrawlerResponse, ExtractRule
from turbocrawler.engine.control import StopCrawler

from crawler.distritos import DISTRITOS_PORTUGAL

from crawler.credentials import HEADERS, COOKIES
from crawler.parsers.idealista_parser import house_parser
from crawler.idealista_crawler import IdealistaCrawler


class IdealistaPTCrawler(IdealistaCrawler):
    crawler_name = "IdealistaPTCrawler"
    allowed_domains = ['idealista.pt']
    main_url = 'https://www.idealista.pt'
    regex_extract_rules = [
        ExtractRule(r'https://www.idealista.pt/arrendar-casas/[a-z-]+-distrito/pagina-[0-9]+', remove_crawled=True),
        ExtractRule(r'https://www.idealista.pt/imovel/[0-9]+')
    ]
    time_between_requests = 1

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

    def parse(self, crawler_request: CrawlerRequest, crawler_response: CrawlerResponse) -> None:
        if 'imovel' in crawler_response.url:
            house_parser(crawler_response)
