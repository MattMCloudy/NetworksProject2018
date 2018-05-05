import threading
import logging
import socket
import time

class ClientServer(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        self.name = args[0]
        self.id = args[1]
        self.routing_table = args[2]
        self.sockets = {}

    def listen(self):
        host = ''
        port = int(self.id)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        threads = []

        while True:
            s.listen(1)
            connection, address = s.accept()
            logging.debug('Listening for incoming messages: '+address)
            new_thread = threading.Thread(self.process_messages(connection, address))
            threads.append(new_thread)

        for t in threads:
            t.join()

    def run(self):
        self.build_connections()
        self.listen()

    def build_connections(self):
        routes = {'Ann': 111, 'Chan': 001, 'Jan': 100, 'A': 8000, 'B':8001,
                  'C': 8002, 'D': 8003, 'E': 8004, 'F': 8005, 'G': 8006,
                  'H': 100, 'L': 8007}
        for name, dist in self.routing_table[self.name].items():
            logging.debug('Connecting to '+name+' at port '+routes[name])
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(routes[name])
            self.sockets[name] = s
            logging.debug('Success')

    def process_messages(self, connection, address):
        #Method to be overridden by child classes
        logging.debug('Generic process method exectued, Error')
        raise NotImplementedError
