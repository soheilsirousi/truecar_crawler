import pika


class ProducerQueue:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            instance = super(ProducerQueue, cls).__new__(cls)
        return instance

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

    def send_message(self, message=''):
        self.channel.queue_declare(queue='default')
        self.channel.basic_publish(exchange='', routing_key='default', body=message)

    def __del__(self):
        self.connection.close()

