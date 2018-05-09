import logging
import socket
import threading
import time



class ClientServer(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=()):
        threading.Thread.__init__(self, group=group, target=target, name=name)
        self.name = args[0]
        self.routes = args[1]
        self.routing_table = args[2]
        self.graph = args[3]
        self.sockets = {}
        self.log = logging.getLogger(self.name)
        self.shutdown_event = threading.Event()

    def listen(self):
        host = ''
        port = self.routes[self.name]
        self.log.debug('Attempting to listen on port: '+str(port))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        threads = []

        while not self.shutdown_event.isSet():
            s.listen(1)
            connection, address = s.accept()
            self.log.debug('Listening for incoming messages: '+str(address[1]))
            new_thread = threading.Thread(name='process_message_'+self.name, target=self.process_messages, args=(connection, address,))
            new_thread.start()
            threads.append(new_thread)

        for t in threads:
            t.join()

    def run(self):
        self.log.debug('new logger: '+self.name)
        listen_thread = threading.Thread(name='listen_'+self.name, target=self.listen)
        build_thread = threading.Thread(name='build_'+self.name, target=self.build_connections)
        listen_thread.start()
        time.sleep(10)
        build_thread.start()
        build_thread.join()
        listen_thread.join()

    def build_connections(self):
        self.log.debug('Building connections to attached routes')
        for name, dist in self.routing_table[self.name].items():
            self.log.debug('Connecting to '+name+' at port '+str(self.routes[name]))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('', self.routes[name]))
            self.sockets[name] = s
            self.log.debug('Success')
        self.log.debug('Finished building connections')

    def shutdown(self):
        for name, socket in self.sockets.items():
            socket.shutdown(0)
            socket.close()
        self.shutdown_event.set()

    def process_messages(self, connection, address):
        #Method to be overridden by child classes
        logging.debug('Generic process method executed, Error')
        raise NotImplementedError
