import json
from client_server import ClientServer

class Agent(ClientServer):
    def process_messages(self, connection, address):
        while True:
            data_json = connection.recv(1024)
            if not data: break
            data = json.loads(data_json.decode())