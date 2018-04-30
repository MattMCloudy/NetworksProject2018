import threading
import logging

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')

class Agent(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        logging.debug('Thread initialized')
        self.agent_name = args[0]
        self.id = args[1]
        self.routing_table = args[2]

    def run(self):
        logging.debug('running')
        return

    def send_message(self, filename):
        message = ''
        with open(filename) as f:
            for line in f:
                do_something_with = line
                #Do some shit

        logging.debug('Message Sent: '+message)

    def receive_message(self, message):
        logging.debug('Message Received: '+message)
        self.send_message('Some sort of acknowledgment')