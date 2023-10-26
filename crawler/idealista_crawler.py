import requests
from turbocrawler import Crawler, CrawlerRequest, CrawlerResponse, CrawlerRunner, ExtractRule, ExecutionInfo
from turbocrawler.engine.control import StopCrawler
from turbocrawler.engine.runners.thread_runner import ThreadCrawlerRunner
from turbocrawler.queues.crawled_queue import MemoryCrawledQueue
from turbocrawler.queues.crawler_queues import FIFOMemoryCrawlerQueue

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
    time_between_requests = 1

    session: requests.Session

    @classmethod
    def start_crawler(cls) -> None:
        cls.session = requests.session()

    @classmethod
    def crawler_first_request(cls) -> CrawlerResponse | None:
        for distrito in DISTRITOS_PORTUGAL:
            url = f'https://www.idealista.pt/arrendar-casas/{distrito}-distrito/pagina-1'
            crawler_request = CrawlerRequest(url=url)
            cls.crawler_queue.add(crawler_request=crawler_request)

        url = "https://www.idealista.pt"
        response = cls.session.get(url=url, headers=HEADERS, cookies=COOKIES)
        return None

    @classmethod
    def process_request(cls, crawler_request: CrawlerRequest) -> CrawlerResponse:
        response = cls.session.get(crawler_request.url, headers=HEADERS, cookies=COOKIES)
        if response.status_code != 200:
            raise StopCrawler("response.status_code != 200")
        return CrawlerResponse(url=response.url,
                               body=response.text,
                               status_code=response.status_code)

    @classmethod
    def parse_crawler_response(cls, crawler_request: CrawlerRequest, crawler_response: CrawlerResponse) -> None:
        if 'imovel' in crawler_response.url:
            house_parser(crawler_response)

    @classmethod
    def stop_crawler(cls, execution_info: ExecutionInfo) -> None:
        cls.session.close()


crawler = IdealistaCrawler
crawled_queue = MemoryCrawledQueue(crawler_name=crawler.crawler_name, save_crawled_queue=True, load_crawled_queue=True)
crawler_queue = FIFOMemoryCrawlerQueue(crawler_name=crawler.crawler_name, crawled_queue=crawled_queue)
CrawlerRunner(crawler=crawler, crawler_queue=crawler_queue).run()
