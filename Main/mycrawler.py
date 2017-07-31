from urllib import request
from urllib import error
from collections import deque
import urllib.parse as urlparse
import re
import datetime
import time


class MySpider:
    def __init__(self, user_agent="cheng",delay = 1):
        self.user_agent = user_agent
        self.num_retries = 0
        self.crawl_queue = deque([])
        self.delay = DelayTime(delay)

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

    def link_crawler(self, seed_url, link_regex,max_depth=2):
        seen = {}
        self.crawl_queue.append(seed_url)
        seen[seed_url]=0
        while self.crawl_queue:
            url = self.crawl_queue.pop()
            self.delay.wait(url)
            html = self.download(url)
            depth = seen[url]
            if depth != max_depth:
                for link in self.get_links(html):
                    if re.match(link_regex,link):
                        link=urlparse.urljoin(seed_url,link)
                        seen[link] = depth+1
                        self.crawl_queue.append(link)
        return seen.keys()

    def get_links(self,html):
        webpage_regex = re.compile(r'''<a[^>]+href=["¥'](.*?)["¥']''',re.IGNORECASE)
        return webpage_regex.findall(html)

class DelayTime:
    def __init__(self,delay):
        self.delay = delay
        self.netAddress = {}
    def wait(self,url):
        netAddress = urlparse.urlparse(url).netloc #获得网址
        last_accessed = self.netAddress.get(netAddress)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now()-last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.netAddress[netAddress] = datetime.datetime.now()




if __name__ == '__main__':
    test = MySpider()
    urls=test.link_crawler(r"http://example.webscraping.com/index","/places/default/(index|view)")
    for url in urls:
        print(url)
