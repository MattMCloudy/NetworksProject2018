import threading
import logging
import time

class Client(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        logging.debug('Thread initialized')
        self.label = args[0]
        self.routing_table = args[1]
        self.message_queue = []
        self.lock = threading.Lock()

    def run(self):
        logging.debug('running')
        self.listen()
        return

    def receive_message(self, message):
        self.lock.acquire()
        self.message_queue.append(message)
        self.lock.release()

    def listen(self):
        logging.debug('Listening for incoming messages')
        while(True):
            self.lock.acquire()
            if self.message_queue:
                for message, i in enumerate(self.message_queue):
                    self.process_message(message)
                    self.message_queue.remove(i)
            self.lock.release()
            time.sleep(0.5)

    def process_message(self, message):
        #TODO
        return 1

    def route(self, message):
        #TODO
        return ''