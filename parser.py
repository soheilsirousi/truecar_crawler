from bs4 import BeautifulSoup
import requests
from database import MongoHandler
from datetime import datetime


class Parser:

    def __init__(self):
        self.soup = None
        self.year = None

    def page_parser(self):
        db = MongoHandler()
        dialogs = db.get_links()
        for dialog in dialogs:
            html = requests.get(dialog['link']).text
            self.soup = BeautifulSoup(html, 'html.parser')
            data = {'name': self.name, 'year': self.year, 'exterior_color': self.exterior_color,
                    'interior_color': self.interior_color, 'distance_traveled': self.distance_traveled,
                    'fuel_type': self.fuel_type, 'price': self.price, 'created_time': str(datetime.now())}
            db.insert_data(data)
            db.visit_link(dialog['link'])

    @property
    def name(self):
        selector = '#mainContent > div:nth-child(1) > div.flex.flex-col-reverse.md\:mt-3.md\:flex-col > div.block.mb-3.hidden.md\:block > h1 > div.heading-3_5.normal-case.heading-md-2.md\:normal-case.grow.leading-\[1\.2\].mb-1'
        _name = self.soup.select_one(selector).text
        self.year = int(_name[:4])
        return _name[5:]

    @property
    def exterior_color(self):
        selector = '#mainContent > div.relative > div.container > div.relative.md\:pt-5.lg\:flex.lg\:flex-row-reverse > div.lg\:w-\[calc\(100\%-375px\)\].lg\:pr-6.xl\:pr-7 > div.mt-4.mb-2.lg\:mt-0 > div > div:nth-child(1) > div > div.flex.items-center'
        ext_color = self.soup.select_one(selector).text
        if ext_color.startswith('Exterior: '):
            return ext_color[10:]
        return ext_color

    @property
    def interior_color(self):
        selector = '#mainContent > div.relative > div.container > div.relative.md\:pt-5.lg\:flex.lg\:flex-row-reverse > div.lg\:w-\[calc\(100\%-375px\)\].lg\:pr-6.xl\:pr-7 > div.mt-4.mb-2.lg\:mt-0 > div > div:nth-child(2) > div > div'
        int_color = self.soup.select_one(selector).text
        if int_color.startswith('Interior: '):
            return int_color[10:]
        return int_color

    @property
    def distance_traveled(self):
        selector = '#mainContent > div.relative > div.container > div.relative.md\:pt-5.lg\:flex.lg\:flex-row-reverse > div.lg\:w-\[calc\(100\%-375px\)\].lg\:pr-6.xl\:pr-7 > div.mt-4.mb-2.lg\:mt-0 > div > div:nth-child(3) > div > div'
        dist_traveled = self.soup.select_one(selector).text.replace(' miles', '')
        return int(dist_traveled.replace(',', ''))

    @property
    def fuel_type(self):
        selector = '#mainContent > div.relative > div.container > div.relative.md\:pt-5.lg\:flex.lg\:flex-row-reverse > div.lg\:w-\[calc\(100\%-375px\)\].lg\:pr-6.xl\:pr-7 > div.mt-4.mb-2.lg\:mt-0 > div > div:nth-child(4) > div > div'
        _fuel_type = self.soup.select_one(selector).text.replace('Fuel Type: ', '')
        return _fuel_type if _fuel_type else None

    @property
    def price(self):
        selector = '#mainContent > div.relative > div.container > div.relative.md\:pt-5.lg\:flex.lg\:flex-row-reverse > div.relative.z-\[9\].ml-auto.w-full.lg\:max-w-\[375px\] > div > div:nth-child(2) > div > div > div.heading-2.normal-case.flex.h-\[40px\].items-center'
        _price = self.soup.select_one(selector).text.replace('$', '')
        return int(_price.replace(',', ''))


if __name__ == '__main__':
    par = Parser()
    par.page_parser()