from turbocrawler import CrawlerRunner, ExtractRule, ExecutionInfo
from turbocrawler.engine.data_types.crawler_runner_config import CrawlerRunnerConfig
from turbocrawler.queues.crawled_queue import MemoryCrawledQueue
from turbocrawler.queues.crawler_queues import FIFOMemoryCrawlerQueue
from crawler.pt_crawler import IdealistaPTCrawler
from crawler.es_crawler import IdealistaESCrawler

config = CrawlerRunnerConfig(crawler_queue=FIFOMemoryCrawlerQueue,
                             crawler_queue_params=None,
                             crawled_queue=MemoryCrawledQueue,
                             crawled_queue_params=dict(save_crawled_queue=True, load_crawled_queue=False),
                             plugins=None, qtd_parse=2)

# result = CrawlerRunner(crawler=IdealistaPTCrawler, config=config).run()
result = CrawlerRunner(crawler=IdealistaESCrawler, config=config).run()
print(result)
