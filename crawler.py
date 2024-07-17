from bs4 import BeautifulSoup
import requests
from database import MongoHandler
from conf import CARS_URL, BASE_URL
from producer import ProducerQueue
import threading
import time


class Crawler:

    @classmethod
    def crawl_page(cls, page_number=1):
        db = MongoHandler()
        context = requests.get(CARS_URL + str(page_number))
        soup = BeautifulSoup(context.text, 'html.parser')
        urls = soup.find_all('a', attrs={'data-test': "vehicleCardLink"})
        for url in urls:
            if not db.link_exist(BASE_URL + url['href']):
                cls.call_queue(url['href'])

    @staticmethod
    def db_save(ch, method, properties, body):
        db = MongoHandler()
        db.insert_link(BASE_URL + body.decode())
        ch.basic_ack(delivery_tag=method.delivery_tag)

    @classmethod
    def call_queue(cls, url):
        q = ProducerQueue()
        q.send_message(url)

    @classmethod
    def deep_crawler(cls, page_limit=2):
        threads = list()
        for i in range(1, page_limit+1):
            th = threading.Thread(target=cls.crawl_page, args=(i, ))
            threads.append(th)
            th.start()

        for thread in threads:
            thread.join()


if __name__ == '__main__':
    Crawler.deep_crawler(page_limit=10)
