import threading
import logging
import time
import socket

class Server(threading.Thread):
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

    def process_messages(self, connection, address):
        while True:
            data = connection.recv(1024)
            if not data:
                break
            else:
                logging.debug('Data to be sent: ' + data)
                connection.send(data)
        connection.close()

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