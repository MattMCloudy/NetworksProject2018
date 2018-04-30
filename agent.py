import threading
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')

class Agent(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        logging.debug('Thread initialized')
        self.agent_name = args[0]
        self.id = args[1]
        self.routing_table = args[2]
        self.message_queue = []
        self.lock = threading.Lock()

    def run(self):
        logging.debug('running')
        self.listen()
        return

    def process_message(self, message):
        #TODO
        return 1

    def send_message(self, filename):
        message = ''
        with open(filename) as f:
            for line in f:
                do_something_with = line
                #Do some shit

        logging.debug('Message Sent: '+message)

    def listen(self):
        logging.debug('Listening for incoming messages')
        while(True):
            self.lock.acquire()
            if self.message_queue:
                for message, i in enumerate(self.message_queue):
                    logging.debug('Message Received: '+message)
                    self.process_message(message)
                    self.message_queue.remove(i)
            self.lock.release
            time.sleep(0.5)

    def receive_message(self, message):
        self.lock.acquire()
        self.message_queue.append(message)
        self.lock.release()