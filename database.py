import pymongo
from datetime import datetime


class MongoHandler:

    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client.get_database('truecar_crawler')
        self.collection = self.db.cars_link

    def insert_link(self, link):
        return self.collection.insert_one({'link': link, 'created_time': str(datetime.now()), 'is_visited': False}).inserted_id

    def visit_link(self, link):
        return self.collection.update_one({'link': link}, {'$set': {'is_visited': True}}, upsert=False)

    def get_links(self, limit=33):
        return self.collection.find({'is_visited': False}).limit(limit)

    def insert_data(self, data):
        return self.db.cars_data.insert_one(data)


if __name__ == '__main__':
    pass
