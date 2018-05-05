from client_server import ClientServer
class Agent(ClientServer):
    def process_messages(self, connection, address):
        return 1