from bs4 import BeautifulSoup
import requests
from database import MongoHandler
from conf import CARS_URL, BASE_URL


class Crawler:

    @classmethod
    def crawl_page(cls, page_number=1):
        context = requests.get(CARS_URL + str(page_number))
        soup = BeautifulSoup(context.text, 'html.parser')
        cls.db_save(soup.find_all('a', attrs={'data-test': "vehicleCardLink"}))

    @classmethod
    def db_save(cls, links):
        db = MongoHandler()
        for link in links:
            db.insert_link(BASE_URL + link['href'])


if __name__ == '__main__':
    Crawler.crawl_page()
