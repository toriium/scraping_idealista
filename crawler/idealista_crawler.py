import requests
from turbocrawler import Crawler, CrawlerRequest, CrawlerResponse, CrawlerRunner, ExtractRule, ExecutionInfo
from turbocrawler.engine.control import StopCrawler
from turbocrawler.queues.crawled_queue import MemoryCrawledQueue
from turbocrawler.queues.crawler_queues import FIFOMemoryQueue

from crawler.distritos import DISTRITOS_PORTUGAL

from crawler.credentials import HEADERS, COOKIES
from crawler.idealista_parser import house_parser


class IdealistaCrawler(Crawler):
    crawler_name = "IdealistaCrawler"
    allowed_domains = ['idealista.pt']
    main_url = 'https://www.idealista.pt'
    regex_extract_rules = [
        ExtractRule(r'https://www.idealista.pt/arrendar-casas/[a-z-]+-distrito/pagina-[0-9]+', remove_crawled=True),
        ExtractRule(r'https://www.idealista.pt/imovel/[0-9]+')
    ]
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
        if response.status_code != 200:
            raise StopCrawler()
        return CrawlerResponse(site_url=response.url,
                               site_body=response.text,
                               status_code=response.status_code)

    def parse_crawler_response(self, crawler_response: CrawlerResponse) -> None:
        if 'imovel' in crawler_response.site_url:
            house_parser(crawler_response)

    def stop_crawler(self, execution_info: ExecutionInfo) -> None:
        self.session.close()


crawler = IdealistaCrawler
crawled_queue = MemoryCrawledQueue(crawler_name=crawler.crawler_name, save_crawled_queue=True, load_crawled_queue=True)
crawler_queue = FIFOMemoryQueue(crawler_name=crawler.crawler_name, crawled_queue=crawled_queue)
CrawlerRunner(crawler=crawler, crawler_queue=crawler_queue).run()
