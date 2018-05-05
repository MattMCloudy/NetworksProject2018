from client_server import ClientServer

class Base(ClientServer):
    def process_messages(self, connection, address):
        return 1