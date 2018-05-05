from client_server import ClientServer

class Router(ClientServer):
    def process_messages(self, connection, address):
        return 1