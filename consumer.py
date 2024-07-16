import pika
from crawler import Crawler


class ConsumerQueue:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            instance = super(ConsumerQueue, cls).__new__(cls)
        return instance

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

    def receive(self, func):
        self.channel.queue_declare(queue='default')
        self.channel.basic_consume(queue='default', on_message_callback=func)
        self.channel.start_consuming()


if __name__ == '__main__':
    q = ConsumerQueue()
    q.receive(func=Crawler.db_save)
