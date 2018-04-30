import threading
import logging

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

class Router(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        logging.debug('Thread initialized')
        self.label = args[0]
        self.routing_table = args[1]

    def run(self):
        logging.debug('running')