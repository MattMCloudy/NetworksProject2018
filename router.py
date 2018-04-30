import logging

class router():
    def __init__(self, label, routing_table):
        logging.debug('Thread initialized')
        self.label = label
        self.routing_table = routing_table