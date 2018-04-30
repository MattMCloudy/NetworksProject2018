import logging

class agent():
    def __init__(self, name, id, routing_table):
        logging.debug('Thread initialized')
        self.name = name
        self.id = id
        self.routing_table = routing_table