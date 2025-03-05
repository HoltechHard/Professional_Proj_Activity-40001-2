from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig

class WebScrapper:
    def __init__(self):
        pass
    
    async def crawl(self, url):
        crawler_config = CrawlerRunConfig(cache_mode = CacheMode.BYPASS)

        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url = url, config = crawler_config)

            return result.markdown
        