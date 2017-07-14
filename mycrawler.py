from urllib import request
from urllib import error
from collections import deque
import re


class MySpider:
    def __init__(self, user_agent="hao"):
        self.user_agent = user_agent
        self.num_retries = 0
        self.crawl_queue = deque([])

    def download(self, url, retry_num=2):
        print("downloading...")
        headers = {"User-Agent": self.user_agent}
        try:
            # Open the URL url, which can be either a string or a Request object.
            request_url = request.Request(url, headers=headers)
            html = request.urlopen(request_url).read()
            # html = request.urlopen(self.url).read()
        except error.URLError as e:
            print("URL Error informtion :" + str(e.reason))
            if retry_num > 0:
                self.download(retry_num - 1)
            html = None
        return html.decode()

    def link_crawler(self, seed_url, link_regex):
        self.crawl_queue.append(seed_url)
        if self.crawl_queue:
            url = self.crawl_queue.pop()
            html = self.download(url)
            for link in self.get_links(html):
                if re.match(link_regex,link):
                    self.crawl_queue.append(link)

    def get_links(self,html):
        webpage_regex = re.compile(r'''<a[^>]+href=["'](.*?)["']''',re.IGNORECASE)
        return webpage_regex.findall(html)


if __name__ == '__main__':
    test = MySpider()
    test.link_crawler(r"http://www.bilibili.com/ranking","//www.bilibili.com/")
    for url in test.crawl_queue:
        print(url)
